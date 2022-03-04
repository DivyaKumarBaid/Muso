import discord
import os
from discord.ext import commands, tasks


# initialising client of the bot
client = commands.Bot(command_prefix='s.', help_command=None)

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
