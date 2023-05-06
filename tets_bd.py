from bot.sql_db import BotDB
BotDB = BotDB('test_db.db')
# BotDB.add_user(599974400)
print(BotDB.set_max_price(555, 55))
print(BotDB.set_min_price(555, 11))
print(BotDB.get_borders(555))
