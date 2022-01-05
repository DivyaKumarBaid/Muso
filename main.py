import os
from keep_alive import keep_alive
import discord
import nacl
from discord import FFmpegPCMAudio
import youtube_dl
import discord.utils
from discord.utils import find
from discord.ext import commands, tasks
from itertools import cycle
from youtubesearchpython import VideosSearch
import numpy as np

#initializing variables

my_secret = os.environ['TOKEN']

client = commands.Bot(command_prefix='m.',help_command=None)

last_vol=[]

song_played=[]

chvc=[]

song_url=[]

voice_channel_to_connect=[]

command_dict = {
  "m.add [url]/[name]" : "Adds given music to queue",
  "m.songs" : "Lists all the songs in the playlist",
  "m.skip" : "Skips the Currently Playing Song",
  "m.play [VoiceChannel]" : "This command plays music in the desired channel",
  "m.play_this [Name]/[URL]" : "Plays a particular song",
  "m.stop" : "Stops the music player",
  "m.remove [index]" : "Removes the particular song at that index",
  "m.clear_playlist" : "Removes every song from the playlist",
  "m.volume [integer value]" : "Sets the volume level",
  "m.playOn [VoiceChannel]" : "Sets the Voice Channel on which bot plays"
}

#initializing variables


# For accessing already created playlist if present

if (os.path.exists('playlist.txt')):
  playlist_ini = np.loadtxt('playlist.txt' , dtype=str , delimiter = '\n')
  playlist_ini = playlist_ini.tolist()

  if(type(playlist_ini)!=list):
    playlist = []
    playlist.append(playlist_ini)
  else:
    playlist = playlist_ini

else:
  f = open("playlist.txt", "x")
  f.close()
  playlist = []

for i in playlist:
  song_url.append(i)
# print(song_url)


# For accessing already created playlist if present

# ffmpeg
#before running install pip install pynacl
#for audio pip install ffmpeg
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'} #locking options for ffmpeg


#when bot is ready
@client.event
async def on_ready():
  print("I am alive")
  last_vol.append(100.0)
  await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game('Music. To know more type m.help'))


#when it is first added to a server
@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        text = discord.Embed(
          title = f'Hello **{guild.name}**!\n',
          url = "https://github.com/DivyaKumarBaid/Discord_music_bot_V-2",
          description = f'Nice to you all.\nTo setup this bot you just need to set the voice channel to play the song by typing m.playOn <channel_name> and add your song by m.add <song_name> and just m.play to play on your channel\nFor more info type m.help',
          color= 53380,
        )
        text.set_author(name= "Discord_music_bot",
        icon_url= "https://img.icons8.com/color/48/000000/phonograph.png")
        text.set_footer(text= "m.help to know commands")

        await general.send(embed=text)



# removes any duplicate songs that is currently in the playlist
def duplicate():
  res = []
  for i in playlist:
    if i not in res:
      res.append(i)
  playlist.clear()
  for i in res:
    playlist.append(i)
# removes any duplicate songs that is currently in the playlist


#infinite loop to play music 24X7 untill closed/stopped 
@tasks.loop(seconds=5)
async def play_song(ctx, ch, channel,l):

  voice = discord.utils.get(client.voice_clients, guild=ctx.guild) 
  
  # print(song_url)

  if len(song_url) == 0:
    duplicate()
    for i in playlist:
      song_url.append(i)
    song_played.clear()

  url=song_url[0]
  
  if not ch.is_playing() and not voice == None :
    try: 
      ydl_opts = {'format': 'bestaudio/best'}
      with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_title = info.get('title', None)
        URL = info['formats'][0]['url']
        
      ch.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)))
      voice.source.volume = last_vol[0]
      text = embedding(f" Playing :{video_title}")
      await ctx.send(embed=text, delete_after=60.0)
      song_played.append(song_url[0])
      song_url.pop(0)
    except:
      await ctx.send("Connection Error!!")

  

#sets the bot to play on a particular channel
@client.command()
async def playOn(ctx,*,channel):
  channel = discord.utils.get(ctx.guild.voice_channels, name=channel)
  if(channel is not None):
    voice_channel_to_connect.clear()
    voice_channel_to_connect.append(channel)
    await ctx.send(f"{channel} is now set to play it Loud ! ")
  else:
    await ctx.send("**Couldnt Find the Channel**")


#skip a song
@client.command(help= "Skip the current song")
async def skip(ctx):
  ch=chvc[0]
  ch.stop()


#sets volume to user defined value and this needs to be refined
@client.command()
async def volume(ctx, x: int):
  if 0 <= x <= 100:
    y=x/100.0
    last_vol.pop(0)
    last_vol.append(y)
    vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
    vc.source.volume = float(y)
    text = discord.Embed(
    title= "**Volume Control**",
    description = f" Volume set to {int(x)} ",
    color= 53380,
    )
    text.set_author(name= "Discord_music_bot",
    icon_url= "https://img.icons8.com/color/48/000000/phonograph.png")
    text.set_footer(text= "m.help to know commands")
    await ctx.send(embed=text)
  else:
    await ctx.send("Volume level must be between 0 to 100")


#play command to start an infinite loop
@client.command(help="Channel name is optional." , brief="This command plays song from the available ones.Providing channel name is optional without which it will play on General")
async def play(ctx, channel = None):
 #joining the desired channel

  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

  channel = discord.utils.get(ctx.guild.voice_channels, name=channel)

  if channel is None:
    if(len(voice_channel_to_connect) == 0):
      await ctx.send(f"Couldnt the channel you told to join please set the channel using m.voice_channel <channel_name> or just pass it as argument in this command")
      return

    else:
      channel = voice_channel_to_connect[0]


  #checking if it is playing any audio
  if voice == None:
    await ctx.send(f"Joined **{channel}**")
  else:
    await ctx.voice_client.disconnect()
  ch = await channel.connect()
  if(len(chvc)!=0):
    chvc.pop(0)
  chvc.append(ch)
  await ctx.send(f"Playing on **{channel}** Channel")
  
  #get the number of songs and if none is present it will show up a message
  duplicate()
  n = len(song_url)
  if not n==0:
    n=n-1
    play_song.start(ctx, ch, channel,n)
  else:
    text = discord.Embed(
    title= "**No Music**",
    description = "There is no music to play\nUse _add [url] to add a music",
    color= 53380,
    )
    text.set_author(name= "Discord_Music_bot",
    icon_url= "https://img.icons8.com/color/48/000000/phonograph.png")
    text.set_footer(text= "m.help to know commands")
    await ctx.send(embed=text)
    
    
#plays a particular music
@client.command(help = "This stops the loop of playing song and plays the mentioned named song instead")
async def play_this(ctx,channel = None,*,name):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild) 
    channel = discord.utils.get(ctx.guild.voice_channels, name=channel)

    if channel is None:
      if(len(voice_channel_to_connect) == 0):
        await ctx.send(f"Couldnt the channel you told to join please set the channel using m.voice_channel <channel_name> or just pass it as argument in this command")
        return

      else:
        channel = voice_channel_to_connect[0]

    if len(chvc)==0 and voice == None:
      ch = await channel.connect()
      chvc.clear()
      chvc.append(ch)
    else :
      ch=chvc[0]
      ch.stop()
    play_song.stop()

    videosSearch = VideosSearch(name, limit = 1)
    result_song_list = videosSearch.result()

    title_song = result_song_list['result'][0]['title']
    urllink = result_song_list['result'][0]['link']
    
    try: 
      ydl_opts = {'format': 'bestaudio/best'}
      with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(urllink, download=False)
        video_title = info.get('title', None)
        URL = info['formats'][0]['url']
      ch.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)))
      text = embedding(f" Playing :{video_title}")
      await ctx.send(embed=text, delete_after=60.0)
      
    except:
      await ctx.send("Connection Error !!! ",delete_after=60.0)



#add music
@client.command(help='youtube link is required', brief='This adds a music to the playlist. The url must be of youtube')
async def add(ctx, * ,searched_song):

  videosSearch = VideosSearch(searched_song, limit = 1)
  result_song_list = videosSearch.result()

  title_song = result_song_list['result'][0]['title']
  urllink = result_song_list['result'][0]['link']
  thumbnail = result_song_list['result'][0]['thumbnails'][0]['url']


  if(not urllink in playlist):
    playlist.append(urllink)
    song_url.append(urllink)


  text = discord.Embed(
  title= "**Song Added**",
  description = f"{title_song} is added to the Queue\nLink : {urllink}",
  color= 53380,
  )
  text.set_image(url = thumbnail)
  text.set_author(name= "Discord_music_bot",
  icon_url= "https://img.icons8.com/color/48/000000/phonograph.png")
  text.set_footer(text= "m.help to know commands")

  duplicate()
  np.savetxt('playlist.txt',playlist , fmt = '%s')
  content = np.loadtxt('playlist.txt' , dtype=str , delimiter = '\n') 
  content = content.tolist()
  
  await ctx.send(embed=text)
  

#leave vc and stop playing
@client.command(help='This stops the loop' ,brief='This stops the music playing and the bot leaves the voice channel')
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild) 
    if voice == None:
      return
    await ctx.voice_client.disconnect()
    play_song.stop()    
    song_url.clear()
    for i in playlist:
      song_url.append(i)
    song_played.clear()
    await ctx.send("Have left the channel")


#lists song
@client.command(help="This shows the songs present in the directory" ,brief='This command lists all the songs available to play')
async def songs(ctx):
  l=len(playlist)
  if(l==0):
    await ctx.send("No music to play")
  for i in range(0,l):
      videosSearch = VideosSearch(playlist[i], limit = 1)
      result_song_list = videosSearch.result()
      # print(result_song_list)
      title_song = result_song_list['result'][0]['title']
      text = discord.Embed(
      description = f"{i+1}# Song Name : {title_song} ",
      color= 53380,
      )
      text.set_author(name= "Discord_music_bot",
      icon_url= "https://img.icons8.com/color/48/000000/phonograph.png")
      await ctx.send(embed=text)

#removes every song
@client.command(help='The file name should be wiht mp3 extension' , brief='This command removes every0 available song')
async def clear_playlist(ctx):
  song_url.clear()
  playlist.clear()

  np.savetxt('playlist.txt',playlist , fmt = '%s')
  
  text= discord.Embed(
  description="**Playlist cleared**",
  color = 53380,
  )
  text.set_author(name= "Discord_music_bot",
  icon_url= "https://img.icons8.com/color/48/000000/phonograph.png")
  text.set_footer(text= "m.help to know commands")
  await ctx.send(embed=text)


#clear
@client.command(help='This command clears text messages', brief='This command clears given number of messages and by default it clears last 5 text messages')
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    text = embedding("Cleared")
    await ctx.send(embed=text)

#remove a particular song   
@client.command(help='The file name should be wiht mp3 extension' , brief='This command removes the specified file')
async def remove(ctx,x: int):
  x=x-1
  name_of_song=song_url[x]
  videosSearch = VideosSearch(song_url[x], limit = 1)
  result_song_list = videosSearch.result()
  title_song = result_song_list['result'][0]['title']
  text= embedding(f"{title_song} Removed")
  await ctx.send(embed=text)
  pos=0
  for i in playlist:
    pos=pos+1
    if i == name_of_song:
      playlist.pop(pos-1)
      break;

  song_url.pop(x)

  np.savetxt('playlist.txt',playlist , fmt = '%s')


#custom help command
@client.group(invoke_without_command=True)
async def help(ctx):
  text = discord.Embed(
  title= "**HELP TAB**",
  url= "https://github.com/DivyaKumarBaid/Discord_Music_bot",
  color= 53380,
  )
  for x in command_dict : 
    des_cmd = command_dict[x]+'\n'
    text.add_field(name = x , value = des_cmd,inline = True)
    # text.add_field(name = '\n', value = "\n")
  text.set_author(name= "Discord_music_bot",
  icon_url= "https://img.icons8.com/color/48/000000/phonograph.png")
  text.set_footer(text= "m.help to know commands")
  await ctx.send(embed=text)
  
#embeds text  
def embedding(text: str):
  text= discord.Embed(
  description=f"**{text}**",
  color = 53380,
  )
  text.set_author(name= "Discord_music_bot",
  icon_url= "https://img.icons8.com/color/48/000000/phonograph.png")
  text.set_footer(text= "m.help to know commands")
  return(text)
  

# checks for errors
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid Command Used. Type m.help to know the commands'
                       )
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            'Give proper values to the command an argument is missing')

keep_alive() #this keeps the bot alive

#runs bot
client.run(my_secret)
