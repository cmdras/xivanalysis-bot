import discord
import os
from replit import db
import requests
import urllib.parse
import time

client = discord.Client()

def get_user_db_key(user):
  return 'fflogs|{0}'.format(user)

def get_guild_db_key(guild_name, guild_server):
  return 'guild|{0}|{1}'.format(guild_name, guild_server)

def get_timestamp_key(guild_name, guild_server):
  return 'timestamp|{0}|{1}'.format(guild_name, guild_server)

def guild_exists(guild_name, guild_server):
  guild_key = get_guild_db_key(guild_name, guild_server)
  return guild_key in db

def register_guild_in_db(guild_name, guild_server, guild_region):
  if (not guild_exists(guild_name, guild_server)):
    guild_key = get_guild_db_key(guild_name, guild_server)
    db[guild_key] = guild_region
    log_message = "Guild {0} registered!".format(guild_name)
  else:
    log_message = "Guild {0} already registered!".format(guild_name)
  
  return log_message

def get_guild_value(guild_name, guild_server):
  if (not guild_exists(guild_name, guild_server)):
    return False
  return db[get_guild_db_key(guild_name, guild_server)]

def get_guild_reports(guild_name, guild_server):
  region = get_guild_value(guild_name, guild_server)
  if (not region):
    return False
  api_token = os.getenv('FFLOGS_API')
  request_string = "https://www.fflogs.com:443/v1/reports/guild/{0}/{1}/{2}?api_key={3}".format(guild_name, guild_server, region, api_token)
  result = requests.get(request_string)
  return result

def save_timestamp_in_db(guild_name, guild_server):
  db[get_timestamp_key(guild_name, guild_server)] = int(time.time() * 1000)

def get_timestamp_in_db(guild_name, guild_server):
  key = get_timestamp_key(guild_name, guild_server)
  return db[key] if key in db else None

def get_new_guild_reports(guild_name, guild_server):
  if (get_timestamp_key(guild_name, guild_server) not in db):
    save_timestamp_in_db(guild_name, guild_server)
  result = get_guild_reports(guild_name, guild_server)
  if (result.status_code != 200):
    return False
  reports = result.json()
  last_timestamp_checked = get_timestamp_in_db(guild_name, guild_server)
  if (not last_timestamp_checked):
    return False
  new_reports = []
  for report in reports:
    if report['start'] > last_timestamp_checked:
      new_reports.append(report)

  save_timestamp_in_db(guild_name, guild_server)
  return new_reports

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
    guild_name = data[1].strip()
    guild_server = data[2].strip()
    guild_region = data[3].strip()
    
    result = register_guild_in_db(guild_name, guild_server, guild_region)
    await message.channel.send(result)

  if message.content.startswith('$guilds'):
    
    matches = db.prefix("guild")
    await message.channel.send(matches)

  if message.content.startswith('$guildreports'):
    data = message.content.split('-')
    guild_name = data[1].strip()
    guild_server = data[2].strip()

    result = get_new_guild_reports(guild_name, guild_server)
    if (not result):
      await message.channel.send("couldn't find new reports dummy")
    else:
      print(result)
      report_id = result[0]["id"]
      await message.channel.send("Analysis for {0}: https://xivanalysis.com/fflogs/{1}".format(guild_name, report_id))    
    
client.run(os.getenv('TOKEN'))

# Register guild
# Register user
# Get Latest Report of guild
# Message user of found report (if registered)
# Construct xivanalysis url
# Db structure

'''
a guild can have reports

use fflogs api to retrieve reports
'''
