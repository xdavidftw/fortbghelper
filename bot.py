import discord
import os
from discord.ext import commands

TOKEN = os.environ['TOKEN']

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

players = {}

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='.help да видиш всички команди'))
    print('Bot is Ready.')

    @client.command()
    async def h():
        await client.say('```Използвай /nick да си смениш името в сървъра както ти е в Fortnite```')
        await client.say('```Използвай /rank за да получиш ранка си според твоето К/Д```')

    @client.command(pass_context=True)
    async def help(ctx):
        author = ctx.message.author

        embed = discord.Embed(
            colour = discord.Colour.orange()
        )

        embed.set_author(name='Команди')
        embed.add_field(name='/nick', value='Използвай /nick да си смениш името в сървъра както ти е в Fortnite', inline=False)
        embed.add_field(name='/rank', value='Използвай /rank за да получиш ранка си според твоето К/Д', inline=False)
        embed.add_field(name=';play', value=';play и името на песента', inline=False)
        embed.add_field(name=';pause', value=';pause за пауза', inline=False)
        embed.add_field(name=';unpause', value=';unpause за ънпауза', inline=False)
        embed.add_field(name=';leave', value=';leave за премахване на бота от чанела', inline=False)
        embed.add_field(name=';stop', value=';stop за спиране на бота', inline=False)

        await client.send_message(author, embed=embed)

    @client.command(pass_context=True)
    async def clear(ctx, amount=100):
        channel = ctx.message.channel
        messages = []
        async for message in client.logs_from(channel, limit=int(amount) + 1):
            messages.append(message)
        await client.delete_messages(messages)
        await client.say('**Избрания брой Съобщения беше изтрит**')

client.run(TOKEN)
