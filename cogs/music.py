import discord
import os
import nacl
import discord.utils
from discord.utils import find
from discord import FFmpegPCMAudio
from discord.ext import commands, tasks
import numpy as np
import youtube_dl
from youtubesearchpython import VideosSearch

# inside a class we have to pass self


class Music(commands.Cog):

    def __init__(self, client):

        # declaring variables
        self.client = client
        self.volume = []
        self.volume.append(100.0)
        self.vc_connected = []
        self.song_played = []
        self.song_url = []
        self.voice_channel_to_connect = []
        self.playlist = []
        self.logo_url = "https://i.postimg.cc/MTWgJN6P/mini.png"
        self.name = "Muso"
        self.currentsong = "Not playing"

        self.ydl_options = {
            'format': 'bestaudio/best'
        }

        # locking options for ffmpeg
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        # extracting already created playlist

        if (os.path.exists('./playlist.txt')):
            self.playlist_initial = np.loadtxt(
                './playlist.txt', dtype=str, delimiter='\n')
            self.playlist_initial = self.playlist_initial.tolist()

            if(type(self.playlist_initial) != list):
                self.playlist = []
                self.playlist.append(self.playlist_initial)
            else:
                self.playlist = self.playlist_initial
        else:
            f = open("./playlist.txt", "x")
            f.close()

        # extracting already created playlist

        # another instance to operate on without changing the main playlist
        for i in self.playlist:
            self.song_url.append(i)

    # removes any duplicate songs that is currently in the playlist

    def duplicate(self):
        res = []

        for i in self.playlist:
            if i not in res:
                res.append(i)

        self.playlist = res

    # infinite loop to play music 24X7 untill closed/stopped

    @ tasks.loop(seconds=5)
    async def play_song(self, ctx, ch, channel, l):

        # rechecking if the client is connected to a voice channel
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        # rechecking the playlist and removing the duplicate after the songs are being played
        if len(self.song_url) == 0:
            self.duplicate()
            for i in self.playlist:
                self.song_url.append(i)
            self.song_played.clear()

        # taking local Variable for songurl
        url = self.song_url[0]

        # iff the client is not playing
        if not ch.is_playing() and not voice == None:
            try:
                with youtube_dl.YoutubeDL(self.ydl_options) as ydl:
                    info = ydl.extract_info(url, download=False)
                    video_title = info.get('title', None)
                    self.currentsong = video_title
                    URL = info['formats'][0]['url']

                ch.play(discord.PCMVolumeTransformer(
                    discord.FFmpegPCMAudio(URL, **self.FFMPEG_OPTIONS)))

                voice.source.volume = self.volume[0]
                text = discord.Embed(description=f" Playing :{video_title}")
                await ctx.send(embed=text, delete_after=150.0)
                self.song_played.append(self.song_url[0])
                self.song_url.pop(0)
            except:
                await ctx.send("*Something Went Wrong*")

    # play command to start an infinite loop

    @commands.command(help="Channel name is optional.", brief="This command plays song from the available ones.Providing channel name is optional without which it will play on General")
    async def play(self, ctx, channel=None):
        # joining the desired channel

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        channel = discord.utils.get(ctx.guild.voice_channels, name=channel)

        # checking if the desired channel is present in the guild
        if channel is None:

            if(len(self.voice_channel_to_connect) == 0):
                await ctx.send(f"Please specify the Channel")
                return
            else:
                channel = self.voice_channel_to_connect[0]

        # checking if it is playing any audio
        if voice == None:
            await ctx.send(f"Joined **{channel}**")
        else:
            await ctx.voice_client.disconnect()

        # connecting to the desired channel
        connected_channel = await channel.connect()

        # updating the voice channel to connect
        if(len(self.vc_connected) != 0):
            self.vc_connected.pop(0)
        self.vc_connected.append(connected_channel)

        await ctx.send(f"Playing on **{channel}** Channel")

        self.duplicate()

        # get the number of songs and if none is present it will show up a message
        n = len(self.song_url)
        if not n == 0:
            n = n-1
            self.play_song.start(ctx, connected_channel, channel, n)
        else:
            text = discord.Embed(
                title="**No Music**",
                description="There is no music to play\n\nUse m.add [url] to add a music",

            )
            text.set_author(name=self.name,
                            icon_url=self.logo_url)
            text.set_footer(text="\nm.help to know commands")
            await ctx.send(embed=text)

    @commands.command(help='Set the Default Voice Channel')
    async def playOn(self, ctx, *, channel):
        channel = discord.utils.get(ctx.guild.voice_channels, name=channel)
        if(channel is not None):
            self.voice_channel_to_connect.clear()
            self.voice_channel_to_connect.append(channel)
            await ctx.send(embed=discord.Embed(description=f"{channel} is now set to play it Loud !"))
        else:
            await ctx.send("**Couldnt Find the Channel**")

    # add music

    @ commands.command(help='youtube link is required', brief='This adds a music to the playlist. The url must be of youtube')
    async def add(self, ctx, *, searched_song):

        # searching the video on youtube
        videosSearch = VideosSearch(searched_song, limit=1)
        result_song_list = videosSearch.result()
        title_song = result_song_list['result'][0]['title']
        urllink = result_song_list['result'][0]['link']
        thumbnail = result_song_list['result'][0]['thumbnails'][0]['url']

        # checking if any duplicate is present in playlist
        if(not urllink in self.playlist):
            self.playlist.append(urllink)
            self.song_url.append(urllink)

        text = discord.Embed(
            title="**Song Added**",
            description=f"{title_song} is added to the Queue\nLink : {urllink}",

        )
        text.set_image(url=thumbnail)
        text.set_author(name=self.name,
                        icon_url=self.logo_url)
        text.set_footer(text="m.help to know commands")

        # recheckin for duplicate link
        self.duplicate()

        np.savetxt('playlist.txt', self.playlist, fmt='%s')
        content = np.loadtxt('playlist.txt', dtype=str, delimiter='\n')
        content = content.tolist()

        await ctx.send(embed=text)

    @ commands.command(help="Skip the current song", aliases=["next"])
    async def skip(self, ctx):
        ch = self.vc_connected[0]
        ch.stop()

    # sets volume to user defined value and this needs to be refined
    @ commands.command(help='Sets the Volume')
    async def volume(self, ctx, x: int):
        if 0 <= x <= 100:
            y = x/100.0
            self.volume.pop(0)
            self.volume.append(y)
            vc = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
            vc.source.volume = float(y)
            text = discord.Embed(
                title="**Volume Control**",
                description=f" Volume set to {int(x)} "
            )
            text.set_author(name=self.name,
                            icon_url=self.logo_url)
            text.set_footer(text="m.help to know commands")
            await ctx.send(embed=text)
        else:
            await ctx.send("Volume level must be between 0 to 100")

    # leave vc and stop playing
    @ commands.command(help='This stops the loop', aliases=["stop"], brief='This stops the music playing and the bot leaves the voice channel')
    async def leave(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice == None:
            return
        await ctx.voice_client.disconnect()
        self.play_song.stop()
        self.song_url.clear()
        self.currentsong = "Not playing"
        self.song_played.clear()
        for i in self.playlist:
            self.song_url.append(i)
        await ctx.send("Has left the Channel")

    # lists song

    @ commands.command(help="This shows the songs present in the directory", aliases=["list", "playlist", "queue"], brief='This command lists all the songs available to play')
    async def songs(self, ctx):
        l = len(self.playlist)

        if(l == 0):
            await ctx.send("No music to play")
            return

        song_list = ""

        for i in range(0, l):
            videosSearch = VideosSearch(self.playlist[i], limit=1)
            result_song_list = videosSearch.result()
            title_song = result_song_list['result'][0]['title']
            song_list = song_list + \
                f"**{i+1}**# Song Name : **{title_song}**\n\n"

        text = discord.Embed(
            description=song_list,

        )
        text.set_author(name=self.name,
                        icon_url=self.logo_url)
        await ctx.send(embed=text)

    # clears playlist

    @ commands.command(help='The file name should be wiht mp3 extension', brief='This command removes every available song')
    async def clear_playlist(self, ctx):
        self.song_url.clear()
        self.playlist.clear()

        np.savetxt('playlist.txt', self.playlist, fmt='%s')

        text = discord.Embed(
            description="**Playlist cleared**",

        )
        text.set_author(name=self.name,
                        icon_url=self.logo_url)
        text.set_footer(text="m.help to know commands")
        await ctx.send(embed=text)

    @ commands.command(help='The file name should be wiht mp3 extension', brief='This command removes the specified file')
    async def remove(self, ctx, x: int):
        if x > len(self.playlist):
            await ctx.send("The List doesnt have that Song,to get the list use songs command")
            return

        x = x-1

        url_of_song = self.playlist[x]

        videosSearch = VideosSearch(self.playlist[x], limit=1)
        result_song_list = videosSearch.result()
        title_song = result_song_list['result'][0]['title']
        text = discord.Embed(description=f"{title_song} Removed")
        await ctx.send(embed=text)

        pos = 0
        for i in self.song_url:
            pos = pos+1
            if i == url_of_song:
                self.song_url.pop(pos-1)
                break

        self.playlist.pop(x)

        np.savetxt('playlist.txt', self.playlist, fmt='%s')

    @commands.command(brief='shows the current song', aliases=["now", "playing_now", "current_song"])
    async def current(self, ctx):
        text = discord.Embed(description=f"{self.currentsong}")
        await ctx.send(embed=text)


async def setup(client):
    await client.add_cog(Music(client))
