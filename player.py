from replit import db

def get_user_db_key(username):
    return 'player|{0}'.format(username)

class Player:

  def __init__(self, username, name=None, server = None):
    
    self.username = username

    if not name:
      name = db[get_user_db_key(username)].split('|')[0]
    self.name = name

    if not server:
      server = db[get_user_db_key(username)].split('|')[1]
    self.server = server
    
  def get_user_db_value(self):
    return '{0}|{1}'.format(self.name, self.server)

  def get_player_guild_key(self):
    return 'member|{0}'.format(self.username)

  def add_guild_to_player(self, guild):
    db[self.get_player_guild_key()] = guild.get_guild_db_key()

