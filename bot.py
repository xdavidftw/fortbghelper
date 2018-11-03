import discord
from discord.ext import commands

TOKEN = 'NTA4MjU0MTUyMzMwMzEzNzQ4.Dr8pnA.WLEee8pebSy_bkR1dbnYrRpUygg'

client = commands.Bot(command_prefix = '/')

@client.event
async def on_ready():
    print('Bot is Ready.')

    client.run(TOKEN)
