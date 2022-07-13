from mcstatus import JavaServer
import discord
from discord.ext import tasks, commands
import time

#server ip:port
ip='[IP:PORT]'

#discord setup
bot= commands.Bot(command_prefix='>')
bot.remove_command('help')
token='[TOKEN]'

@bot.command()
async def help(ctx):
    help = discord.Embed(title="Commands:", description="**pl** - player list\n**help** - command list\n**legend** - explenation of the bots statuses", color=0xffffff)
    help.set_footer(text='prefix " > "')
    await ctx.send(embed=help)

@bot.command()
async def pl(ctx):
    global q
    names=q.players.names
    namesf=', '.join(str(j) for j in names)
    message=discord.Embed(title="Players:", description=namesf, color=0x00f504)
    await ctx.send(embed=message)

@bot.command()
async def legend(ctx):
    legend = discord.Embed(title='Bots legend:',description='**[Nr] players** - shows how many palyers are playing on server\n**dead server** - shows that the server is empty\n\n💀💀💀💀💀 - shows the the server is offline', color=0x002aff)
    await ctx.send(embed=legend)

@bot.event
async def on_ready():
    print('Starting bot...')
    myLoop.start()

@tasks.loop(seconds = 10)
async def myLoop():
    global q
    #setup and on check
    i=0
    while i<1:
        server = JavaServer.lookup(ip)
        try:
            s = server.status()
            q = server.query()
            i=2

        except TimeoutError:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='💀💀💀💀💀'))
            print('offline')
            i=0
            time.sleep(10)

    #commands
    playerc = s.players.online

    #discord exec
    if playerc>0:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='{} players'.format(playerc)))

    else:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='dead server'))

bot.run(token)
