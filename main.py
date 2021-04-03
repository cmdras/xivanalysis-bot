import discord
import os
from replit import db
from guild import Guild
from player import Player, get_user_db_key

client = discord.Client()

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
    splitMessage = message.content.split('-')
    if len(splitMessage) < 2:
      await message.channel.send("you're potato, invalid command")
      return
    player = Player(message.author, splitMessage[1].strip(), splitMessage[2].strip())
    db[get_user_db_key(message.author)] = player.get_user_db_value()
    await message.channel.send("registered @{0} with player name {1}".format(message.author, player.name))

  if message.content.startswith('$myguild '):
    data = message.content.split('-')
    guild = Guild(data[1].strip(), data[2].strip())
    player = Player(message.author)
    player.add_guild_to_player(guild)
    guild.add_player_to_guild(player)

  if message.content.startswith('$whatsmyguild'):
    player = Player(message.author)
    player_guild = db[player.get_player_guild_key()]
    await message.channel.send(player_guild)

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

  if message.content.startswith('$guildmembers'):
    data = message.content.split('-')
    guild = Guild(data[1].strip(), data[2].strip())
    await message.channel.send(db[guild.get_guild_members_key()])
    
client.run(os.getenv('TOKEN'))
