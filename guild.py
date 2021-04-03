from regions import REGIONS
from replit import db
import time, os, urllib.parse, requests
from player import get_user_db_key

class Guild:

  def __init__(self, name, server):
    self.name = name
    self.server = server
    self.region = REGIONS[server]

  def register_guild_in_db(self):
    if (not self.guild_exists()):
      db[self.get_guild_db_key()] = self.region
      db[self.get_guild_members_key()] = ""
      log_message = "Guild {0} registered!".format(self.name)
    else:
      log_message = "Guild {0} already registered!".format(self.name)
    
    return log_message

  def guild_exists(self):
    guild_key = self.get_guild_db_key()
    return guild_key in db

  def get_guild_db_key(self):
    return 'guild|{0}|{1}'.format(self.name, self.server)

  def get_timestamp_key(self):
    return 'timestamp|{0}|{1}'.format(self.name, self.server)

  def get_guild_members_key(self):
    return 'guildmembers|{0}|{1}'.format(self.name, self.server)

  def get_guild_value(self):
    if (not self.guild_exists()):
      return False
    return db[self.get_guild_db_key()]

  def save_timestamp_in_db(self):
    db[self.get_timestamp_key()] = int(time.time() * 1000)
    
  def get_timestamp_in_db(self):
    key = self.get_timestamp_key()
    return db[key] if key in db else None

  def get_new_guild_reports(self):
    if (self.get_timestamp_key() not in db):
      self.save_timestamp_in_db()
    result = self.get_guild_reports()
    if (result.status_code != 200):
      return False
    reports = result.json()
    last_timestamp_checked = self.get_timestamp_in_db()
    if (not last_timestamp_checked):
      return False
    new_reports = []
    for report in reports:
      if report['start'] > last_timestamp_checked:
        new_reports.append(report)

    self.save_timestamp_in_db()
    return new_reports

  def get_guild_reports(self):
    api_token = os.getenv('FFLOGS_API')
    request_string = "https://www.fflogs.com:443/v1/reports/guild/{0}/{1}/{2}?api_key={3}".format(urllib.parse.quote(self.name), self.server, self.region, api_token)
    result = requests.get(request_string)
    return result

  def add_player_to_guild(self, player):
    db[self.get_guild_members_key()] = db[self.get_guild_members_key()] + '{0}|'.format(player.username)