import os
from keep_alive import keep_alive
import discord
import nacl
from discord import FFmpegPCMAudio
import os
import youtube_dl
import discord.utils
from discord.ext import commands, tasks
from itertools import cycle
from youtubesearchpython import VideosSearch
from lyrics import *
from pymongo import MongoClient


my_secret = os.environ['TOKEN']

client = commands.Bot(command_prefix='m.',help_command=None)
song_played=[]
song_url=[]
playlist=[]
chvc=[]

#before running install pip install pynacl
#for audio pip install ffmpeg

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'} #locking options for ffmpeg

def duplicate():
  res = []
  for i in playlist:
    if i not in res:
      res.append(i)
  playlist.clear()
  for i in res:
    playlist.append(i)


#infinite loop to play music 24X7 untill closed/stopped 
@tasks.loop(seconds=5)
async def play_song(ctx, ch, channel,l):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild) 
  global song_url
  url=song_url[0]
  if not ch.is_playing() and not voice == None :
    try: 
      ydl_opts = {'format': 'bestaudio/best'}
      with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        video_title = info.get('title', None)
        URL = info['formats'][0]['url']
      ch.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
      text = embedding(f" Playing :{video_title}")
      await ctx.send(embed=text, delete_after=60.0)
      song_played.append(song_url[0])
      song_url.pop(0)
    except:
      await ctx.send("Connection Error!!")
  if len(song_url) == 0:
    duplicate()
    for i in playlist:
      song_url.append(i)
    song_played.clear()
  
#skip a song
@client.command(help= "Skip the current song")
async def skip(ctx):
  ch=chvc[0]
  ch.stop()

#when bot is ready
@client.event
async def on_ready():
  print("I am alive")
  await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game('Music. To know more type m.help'))


#sets volume to user defined value and this needs to be refined
@client.command()
async def volume(ctx, x: int):
  y=x/100
  vc = discord.utils.get(client.voice_clients, guild=ctx.guild)
  vc.source = discord.PCMVolumeTransformer(vc.source)
  vc.source.volume = y
  text = discord.Embed(
  title= "**Volume Control**",
  description = f" Volume set to {int(x)} ",
  color= 53380,
  )
  text.set_author(name= "Discord_music_bot",
  icon_url= "https://img.icons8.com/color/48/000000/phonograph.png")
  text.set_footer(text= "m.help to know commands")
  await ctx.send(embed=text)


#play command to start an infinite loop
@client.command(help="Channel name is optional." , brief="This command plays song from the available ones.Providing channel name is optional without which it will play on General")
async def play(ctx, channel='General'):
 #joining the desired channel
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild) 
  channel = discord.utils.get(ctx.guild.voice_channels, name=channel)
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
    


#add music
@client.command(help='youtube link is required', brief='This adds a music to the playlist. The url must be of youtube')
async def add(ctx, * ,searched_song):
  # print(searched_song)

  videosSearch = VideosSearch(searched_song, limit = 1)
  result_song_list = videosSearch.result()

  title_song = result_song_list['result'][0]['title']
  urllink = result_song_list['result'][0]['link']

  song_url.append(urllink)
  playlist.append(urllink)
  text = discord.Embed(
  title= "**Song Added**",
  description = f"{title_song} is added to the Queue\nLink : {urllink}",
  color= 53380,
  )
  # text.add_image(url=f"{result_song_list['result'][0]['thumbnail']['url']}")
  text.set_author(name= "Discord_music_bot",
  icon_url= "https://img.icons8.com/color/48/000000/phonograph.png")
  text.set_footer(text= "m.help to know commands")
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


@client.command(help = "This stops the loop of playing song and plays the mentioned named song instead")
async def play_this(ctx,*,name,channel="General"):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild) 
    channel = discord.utils.get(ctx.guild.voice_channels, name=channel)
    if len(chvc)==0:
      ch = await channel.connect()
    else :
      ch=chvc[0]
      ch.stop()
    play_song.stop()
    # for i in range(0,len(song_played)):
    #   song_url.append(song_played[i])

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
      ch.play(discord.FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
      text = embedding(f" Playing :{video_title}")
      await ctx.send(embed=text, delete_after=60.0)
      
    except:
      await ctx.send("Connection Error !!! ",delete_after=60.0)


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

#custom help command
@client.group(invoke_without_command=True)
async def help(ctx):
  text = discord.Embed(
  title= "**HELP TAB**",
  url= "https://github.com/DivyaKumarBaid/Discord_Music_bot",
  description = "***Welcome to Help Tab. Below are definations and how to use commands section*** \n\n**m.add [url]/[name] ** => This adds the music to queue \n\n**m.play [VoiceChannel(optional)]** => This command plays music in the desired channel or by default in General\n\n**m.songs**  =>  Lists all the songs in the playlist\n\n**m.volume [integer value]** => Sets the volume level\n\n**m.stop** => Stops the music player\n\n**m.clear_playlist** => Removes every song from the playlist\n\n**m.remove [index from the list of songs provided by typing m.songs]** => Removes the particular song\n\n",
  color= 53380,
  )
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
  

# # checks for errors
# @client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.send('Invalid Command Used. Type m.help to know the commands'
#                        )
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send(
#             'Give proper values to the command an argument is missing')

keep_alive() #this keeps the bot alive

#runs bot
client.run(my_secret)
