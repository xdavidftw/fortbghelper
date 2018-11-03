import discord
import youtube_dl
from discord.ext import commands

TOKEN = 'NTA4MjU0MTUyMzMwMzEzNzQ4.Dr8pnA.WLEee8pebSy_bkR1dbnYrRpUygg'

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

        await client.send_message(author, embed=embed)

    @client.command(pass_context=True)
    async def join(ctx):
        channel = ctx.message.author.voice.voice_channel
        await client.join_voice_channel(channel)

    @client.command(pass_context=True)
    async def leave(ctx):
        server = ctx.message.server
        voice_client = client.voice_client_in(server)
        await voice_client.disconnect()

    @client.command(pass_context=True)
    async def clear(ctx, amount=100):
        channel = ctx.message.channel
        messages = []
        async for message in client.logs_from(channel, limit=int(amount) + 1):
            messages.append(message)
        await client.delete_messages(messages)
        await client.say('**Избрания брой Съобщения беше изтрит**')

    @client.command(pass_context=True)
    async def play(ctx, url):
        server = ctx.message.server
        voice_client = client.voice_client_in(server)
        player = await voice_client.create_ytdl_player(url)
        players[server.id] = player
        player.start()

client.run(TOKEN)
