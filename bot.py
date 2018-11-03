import discord
import asyncio
import youtube_dl
import os
from discord.ext import commands
from discord.ext.commands import Bot

TOKEN = 'NTA4MjU0MTUyMzMwMzEzNzQ4.Dr8pnA.WLEee8pebSy_bkR1dbnYrRpUygg'

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

from discord import opus
OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll',
             'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']


def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True

    for opus_lib in opus_libs:
            try:
                opus.load_opus(opus_lib)
                return
            except OSError:
                pass

    raise RuntimeError('Could not load an opus lib. Tried %s' %
                       (', '.join(opus_libs)))
load_opus_lib()

in_voice=[]


players = {}
songs = {}
playing = {}
async def all_false():
    for i in bot.servers:
        playing[i.id]=False

async def checking_voice(ctx):
    await asyncio.sleep(130)
    if playing[ctx.message.server.id]== False:
        try:
            pos = in_voice.index(ctx.message.server.id)
            del in_voice[pos]
            server = ctx.message.server
            voice_client = bot.voice_client_in(server)
            await voice_client.disconnect()
            await bot.say("{} left because there was no audio playing for a while".format(bot.user.name))
        except:
            pass

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
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)
    in_voice.append(ctx.message.server.id)


async def player_in(con):  # After function for music
    try:
        if len(songs[con.message.server.id]) == 0:  # If there is no queue make it False
            playing[con.message.server.id] = False
            bot.loop.create_task(checking_voice(con))
    except:
        pass
    try:
        if len(songs[con.message.server.id]) != 0:  # If queue is not empty
            # if audio is not playing and there is a queue
            songs[con.message.server.id][0].start()  # start it
            await bot.send_message(con.message.channel, 'Now queueed')
            del songs[con.message.server.id][0]  # delete list afterwards
    except:
        pass


@client.command(pass_context=True)
async def play(ctx, *,url):

    opts = {
        'default_search': 'auto',
        'quiet': True,
    }  # youtube_dl options


    if ctx.message.server.id not in in_voice: #auto join voice if not joined
        channel = ctx.message.author.voice.voice_channel
        await bot.join_voice_channel(channel)
        in_voice.append(ctx.message.server.id)

    

    if playing[ctx.message.server.id] == True: #IF THERE IS CURRENT AUDIO PLAYING QUEUE IT
        voice = bot.voice_client_in(ctx.message.server)
        song = await voice.create_ytdl_player(url, ytdl_options=opts, after=lambda: bot.loop.create_task(player_in(ctx)))
        songs[ctx.message.server.id]=[] #make a list 
        songs[ctx.message.server.id].append(song) #add song to queue
        await bot.say("Audio {} is queued".format(song.title))

    if playing[ctx.message.server.id] == False:
        voice = bot.voice_client_in(ctx.message.server)
        player = await voice.create_ytdl_player(url, ytdl_options=opts, after=lambda: bot.loop.create_task(player_in(ctx)))
        players[ctx.message.server.id] = player
        # play_in.append(player)
        if players[ctx.message.server.id].is_live == True:
            await bot.say("Can not play live audio yet.")
        elif players[ctx.message.server.id].is_live == False:
            player.start()
            await bot.say("Now playing audio")
            playing[ctx.message.server.id] = True



@client.command(pass_context=True)
async def queue(con):
    await bot.say("There are currently {} audios in queue".format(len(songs)))

@client.command(pass_context=True)
async def pause(ctx):
    players[ctx.message.server.id].pause()

@client.command(pass_context=True)
async def resume(ctx):
    players[ctx.message.server.id].resume()
          
@client.command(pass_context=True)
async def volume(ctx, vol:float):
    volu = float(vol)
    players[ctx.message.server.id].volume=volu


@client.command(pass_context=True)
async def skip(con): #skipping songs?
  songs[con.message.server.id]
    
    
    
@client.command(pass_context=True)
async def stop(con):
    players[con.message.server.id].stop()
    songs.clear()

@client.command(pass_context=True)
async def leave(ctx):
    pos=in_voice.index(ctx.message.server.id)
    del in_voice[pos]
    server=ctx.message.server
    voice_client=bot.voice_client_in(server)
    await voice_client.disconnect()
    songs.clear()

client.run(TOKEN)
