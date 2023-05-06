from bot.sql_db import BotDB
BotDB = BotDB('test_db.db')
# BotDB.add_user(599974400)
print(BotDB.get_borders(555))
