import discord
import os
from discord.ext import commands, tasks
from discord.utils import find


# initialising client of the bot
client = commands.Bot(command_prefix='m.', help_command=None)

# token obtained from the discord dev portal
my_secret = os.environ.get('TOKEN')

# loads any cogs present
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# when bot is ready and online
@client.event
async def on_ready():
    print("I am alive")
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game('Music. To know more type m.help'))


# on guild join
@client.event
async def on_guild_join(guild):
    general = find(lambda x: x.name == 'general',  guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        text = discord.Embed(
            title=f'Hello **{guild.name}**!\n',
            url="https://github.com/DivyaKumarBaid",
            description=f'**Nice to you all**.\n\nTo setup this bot you just need to set the voice channel to play the song by typing **m.playOn <channel_name>** and add your song by **m.add <song_name>** and just m.play to play on your channel\n\nFor more info type **m.help**',
            color=53380,
        )
        text.set_author(name="Muso",
                        icon_url="https://i.postimg.cc/MTWgJN6P/mini.png")
        text.set_image(url="https://i.postimg.cc/s2Pb8srG/banner.png")
        text.set_footer(text="m.help to know commands")
        await general.send(embed=text)

# commands that loads the cog files


@client.command()
async def load(ctx):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')


# command that reloads the cog files
@client.command()
async def reload(ctx):

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.unload_extension(f'cogs.{filename[:-3]}')

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

# checks for errors


@ client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid Command Used. Type m.help to know the commands'
                       )
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            'Give proper values to the command an argument is missing')


# runs the particular bot
client.run(my_secret)
