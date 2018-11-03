import discord
from discord.ext import commands

TOKEN = 'NTA4MjU0MTUyMzMwMzEzNzQ4.Dr8pnA.WLEee8pebSy_bkR1dbnYrRpUygg'

bot = commands.Bot(command_prefix = '/')

@bot.event
async def on_ready():
    print('Bot is Ready.')

    bot.run(TOKEN)
