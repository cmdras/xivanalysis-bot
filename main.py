import discord
import os
from replit import db
# import requests
# import urllib.parse
# import time
from guild import Guild

client = discord.Client()

def get_user_db_key(user):
  return 'fflogs|{0}'.format(user)

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('potato')

  if message.content.startswith('$iam '):
    splitMessage = message.content.split('$iam ')
    if len(splitMessage) < 2:
      await message.channel.send("you're potato, invalid command")
      return
    
    db[get_user_db_key(message.author)] = splitMessage[1]
    await message.channel.send("registered @{0} with username {1}".format(message.author, splitMessage[1]))

  if message.content.startswith('$registerguild'):
    data = message.content.split('-')
    guild = Guild(data[1].strip(), data[2].strip())
    
    result = guild.register_guild_in_db()
    await message.channel.send(result)

  if message.content.startswith('$guilds'):
    
    matches = db.prefix("guild")
    await message.channel.send(matches)

  if message.content.startswith('$guildreports'):
    data = message.content.split('-')
    guild = Guild(data[1].strip(), data[2].strip())

    result = guild.get_new_guild_reports()
    if (not result):
      await message.channel.send("couldn't find new reports dummy")
    else:
      report_id = result[0]["id"]
      await message.channel.send("Analysis for {0}: https://xivanalysis.com/fflogs/{1}".format(guild.name, report_id))    
    
client.run(os.getenv('TOKEN'))
