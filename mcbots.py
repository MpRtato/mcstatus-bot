from mcstatus import JavaServer
import discord
from discord.ext import tasks, commands
from discord.utils import get
import asyncio

#server ip:port
serverip='[IP:PORT]'

#channel id and role (for role mention)
idc=[CHANNELID]
rolen='[ROLENAME]'

#discord setup
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True

bot= commands.Bot(command_prefix='>', intents=intents)
bot.remove_command('help')
#discord bot token
token='[TOKEN]'

offon = 3 #0-off; 1-on;            3-idle
status=3 #0-off; 1-on has players; 2-on no players;     3-idle

pplayerc=-1

@bot.command()
async def help(ctx):
    help = discord.Embed(title="Commands:", description="**pl** - player list\n**ip** - server ip\n**version** - server version\n**legend** - explenation of the bots statuses\n**help** - command list", color=0xffffff)
    help.set_footer(text='prefix " > "')
    await ctx.send(embed=help)

@bot.command()
async def pl(ctx):
    if on == 1:
        names=q.players.names
        namesf=', '.join(str(j) for j in names)

        if playerc == 0:
            plistoff = discord.Embed(title="Players:",description='**Empty**', color=0xe7eb00)
            plistoff.set_image(url="https://media.tenor.com/j4IbM9Wtk8oAAAAd/dead-server-meme-server-dead.gif")
            
            await ctx.send(embed=plistoff)

        else:
            pliston=discord.Embed(title="Players:", description=namesf, color=0xe7eb00)
            await ctx.send(embed=pliston)

    else:
        offline = discord.Embed(title=" ", description="**Server is offline**", color=0xe60000)
        offline.set_image(url="https://c.tenor.com/EqGmpLByTJEAAAAC/dreaming-key-smash.gif")

        await ctx.send(embed=offline)

@bot.command()
async def ip(ctx):
    if on==1:
        adress = discord.Embed(title="Server IP:", description=serverip, color=0xffffff)
        await ctx.send(embed=adress)
    
    else:
        offline = discord.Embed(title=" ", description="**Server is offline**", color=0xe60000)
        offline.set_image(url="https://c.tenor.com/EqGmpLByTJEAAAAC/dreaming-key-smash.gif")

        await ctx.send(embed=offline)

@bot.command()
async def version(ctx):
    if on==1:
        vers=s.version.name
        versions = discord.Embed(title="Server version:", description=vers, color=0xff4d00)
        await ctx.send(embed=versions)
        
    else:
        offline = discord.Embed(title=" ", description="**Server is offline**", color=0xe60000)
        offline.set_image(url="https://c.tenor.com/EqGmpLByTJEAAAAC/dreaming-key-smash.gif")

        await ctx.send(embed=offline)


@bot.command()
async def legend(ctx):
    legend = discord.Embed(title='Bots legend:',description='**[Nr] players** - shows how many palyers are playing on server\n**dead server** - shows that the server is empty\n\n💀💀💀💀💀 - shows that the server is offline', color=0x002aff)
    await ctx.send(embed=legend)

@bot.event
async def on_ready():
    print('Starting bot...')
    print('[0-off   1-on has players   2-on no players]')
    myLoop.start()

@tasks.loop(seconds = 10)
async def myLoop():
    global status
    global q
    global s
    global on
    global playerc
    global pplayerc
    global offon

    #setup and on check
    i=0
    while i<1:
        server = JavaServer.lookup(serverip)
        try:
            s = server.status()
            q = server.query()

            on = 1
            #server on ping
            #if offon==1:
                #channel = bot.get_channel(id=idc)
                #for guild in bot.guilds:
                    #role = get(guild.roles, name=rolen)
                #ping = discord.Embed(title=" ", description="**Serveris ieslegts**", color=0x44c200)
                #ping.set_image(url='https://c.tenor.com/AbbpfjS0dSgAAAAd/minecraft-twerk.gif')
                #await channel.send(f"{role.mention}", embed=ping)

            offon=0

            i=2


        except (TimeoutError, ConnectionRefusedError):
            if status!=0:
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='💀💀💀💀💀'), status=discord.Status.dnd)
                status=0

            print(status)

            on = 0
            offon=1
            i=0
            await asyncio.sleep(10)

    #commands
    playerc = s.players.online

    #discord exec
    if playerc>0:
        if pplayerc!=playerc:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='{} players'.format(playerc)))
        pplayerc = playerc
        status=1

    else:
        if status!=2:
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='dead server'), status=discord.Status.idle)
            pplayerc = -1
            status=2

    print(status)

bot.run(token)
