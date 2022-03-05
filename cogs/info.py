from dis import disco
import discord
from discord.utils import find
from discord.ext import commands

# inside a class we have to pass self


class Info(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.command_dict = {
            "m.add [url]/[name]": "Adds given music to queue",
            "m.songs": "Lists all the songs in the playlist",
            "m.skip": "Skips the Currently Playing Song",
            "m.play [VoiceChannel]": "This command plays music in the desired channel",
            "m.stop": "Stops the music player",
            "m.remove [index]": "Removes the particular song at that index",
            "m.clear_playlist": "Removes every song from the playlist",
            "m.volume [integer value]": "Sets the volume level",
            "m.playOn [VoiceChannel]": "Sets the Voice Channel on which bot plays"
        }

    # event within a cog
    # function decorator
    @commands.Cog.listener()
    async def on_guild_join(guild):
        general = find(lambda x: x.name == 'general',  guild.text_channels)
        if general and general.permissions_for(guild.me).send_messages:
            text = discord.Embed(
                title=f'Hello **{guild.name}**!\n',
                url="https://github.com/DivyaKumarBaid/Orches",
                description=f'Nice to you all.\nTo setup this bot you just need to set the voice channel to play the song by typing m.playOn <channel_name> and add your song by m.add <song_name> and just m.play to play on your channel\nFor more info type m.help',
                color=53380,
            )
            text.set_author(name="Muso",
                            icon_url="https://i.postimg.cc/MTWgJN6P/mini.png")
            text.set_image(url="https://i.postimg.cc/MTWgJN6P/banner.png")
            text.set_footer(text="m.help to know commands")
            await general.send(embed=text)

    # commands within a cog
    # custom help command

    @ commands.group(invoke_without_command=True)
    async def help(self, ctx):
        text = discord.Embed(
            title="**Commands**",
            url="https://github.com/DivyaKumarBaid/Discord_Music_bot",
            color=53380,
        )
        for x in self.command_dict:
            des_cmd = self.command_dict[x]+'\n'
            text.add_field(name=x, value=des_cmd, inline=True)
        text.set_author(name="Muso",
                        icon_url="https://i.postimg.cc/MTWgJN6P/mini.png")
        text.set_footer(text="m.help to know commands")
        await ctx.send(embed=text)


def setup(client):
    client.add_cog(Info(client))
