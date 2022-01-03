
import os
import io
from datetime import datetime, timedelta
import discord

import time
import requests

import humanize

#from dotenv import load_dotenv
 
USERID = ['<@!926742694435360780>', '<@926742694435360780>']
client = discord.Client()

commands = dict()
################################################################################
################################### commands ###################################
################################################################################

async def cmd_quit(message, cmd, args):
    await message.channel.send("quitting")
    #await client.logout()
    await client.close()
    return
commands['quit'] = cmd_quit

async def cmd_webb(message, cmd, args):
    
    # thanks parse
    # webb-tracker-api container running with dns hostname 'api'
    # it takes a few seconds to load, so retry every second while unavailable
    #API_ENDPOINT = "http://api:8001/track"
    #API_ENDPOINT = "http://localhost:8001/track"
    API_ENDPOINT = "https://api.jwst-hub.com/track"
    API_RETRY_TIMEOUT_SECONDS = 1

    print("polling webb api...")
    r = requests.get(API_ENDPOINT)
    while r.status_code != 200:
        print("api not available, retryingin %d second(s)"%API_RETRY_TIMEOUT_SECONDS)
        time.sleep(API_RETRY_TIMEOUT_SECONDS)
        r = requests.get(API_ENDPOINT)
        
    d = r.json()
    #for k,v in d.items():
    #    print(k, v)

    D = datetime.strptime(d['launchElapsedTime'], '%d:%H:%M:%S')
    D_str = humanize.precisedelta(timedelta(days=D.day, hours=D.hour, minutes=D.minute, seconds=D.second))

    e = discord.Embed(title='James Webb Space Telescope Status', color=discord.Color.gold(), url='https://www.jwst.nasa.gov/content/webbLaunch/whereIsWebb.html')
    #e.set_thumbnail(url=d['deploymentImgURL'])
    ei = discord.Embed(color=discord.Color.gold())
    ei.set_image(url=d['deploymentImgURL'])
    #e.set_image(url=d['deploymentImgURL'])
    e.add_field(name=':gear: Active Deployment Step', value=d['currentDeploymentStep'], inline=False)

    e.add_field(name=':stopwatch: Elapsed Time', value=D_str, inline=True)
    e.add_field(name=':hourglass: Percent Completed', value='%f%%'%d['percentageCompleted'], inline=True)

    pct = d['percentageCompleted'] / 100
    e.add_field(name=u'\U0001F30E' + u'\U00002B1B'*5 + u'\U0001F317' + u'\U00002B1B'*19 + u'\U0001F6F8',
                value=u'\U00002B1B'*int(pct*27) + u'\U0001F6F0' + u'\U00002B1B'*int((1.0-pct)*27), inline=False)
    
    e.add_field(name=':earth_americas: Distance from Earth', value='%f Km'%d['distanceEarthKm'], inline=True)
    e.add_field(name=':satellite_orbital: Distance from L2', value='%f Km'%d['distanceL2Km'], inline=True)
    e.add_field(name=':rocket: Current Speed', value='%f ᴷᴹ/s'%d['speedKmS'], inline=True)
    
    warmString = '%f°C %f°C'%(d['tempC']['tempWarmSide1C'], d['tempC']['tempWarmSide2C'])
    coolString = '%f°C %f°C'%(d['tempC']['tempCoolSide1C'], d['tempC']['tempCoolSide2C'])
    e.add_field(name=':hot_face: Warm Side Temperatures', value=warmString, inline=True)
    e.add_field(name=':cold_face: Cool Side Temperatures', value=coolString, inline=True)

    hpct = max(d['tempC']['tempWarmSide1C'], d['tempC']['tempWarmSide2C'])
    cpct = min(d['tempC']['tempCoolSide1C'], d['tempC']['tempCoolSide2C'])
    hpct = (hpct + 233)/(85+233)
    cpct = (cpct + 233)/(85+233)
    e.add_field(name=u'\U0001F7E5' + u'\U0001F7E5'*int(hpct*27) + u'\U00002B1B'*int((1-hpct)*27),
                value=u'\U0001F7E6' + u'\U0001F7E6'*int(cpct*27) + u'\U00002B1B'*int((1-cpct)*27),
                inline=False)
    
    
    await message.channel.send(embed=ei)
    await message.channel.send(embed=e)

    print()
    #await commands['quit'](message, 'quit', [])
    
    return
commands['webb'] = cmd_webb

################################################################################
################################## main loop ###################################
################################################################################

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    # Check if the message started with @Webb Bot
    conds = [message.content.startswith(USERID[0]), message.content.startswith(USERID[1]),
             message.content.lstrip()[0] == '>', message.content.lstrip()[0] == '!']
    
    if not any(conds):
        return
    
    cut = len(USERID[0])
    if conds[1]:
        cut = len(USERID[1])
    if conds[2] or conds[3]:
        cut = 1
    
    message.content = message.content[cut:].lstrip()
    msg = message.content

    print(message.guild.name)
    print(message.channel.name)
    print(message.author.nick)
    print(msg)

    args = list(map(lambda s: s.strip(), msg.split()))

    if len(args) == 0:
        return await commands['webb'](message, 'webb', args)
    else:
        cmd = args[0]
        args = args[1:]

        if message.author.id != 133719771702099968: #me
            return

        if cmd in commands.keys():
            return await commands[cmd](message, cmd, args)
    
@client.event
async def on_ready():
    global USERID
    USERID[0] = '<@!' + str(client.user.id) + '>'
    USERID[1] = '<@' + str(client.user.id) + '>'
    print('Logged in as')
    print(client.user.name)
    print(USERID[1])
    print('------')

if __name__ == "__main__":
    client.run(os.getenv('WEBB_BOT_DISCORD_TOKEN'))
    
    #file = open("DiscordToken.txt", "r")
    #client.run(file.read())
    #file.close()
    
