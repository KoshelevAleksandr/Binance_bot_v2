import sqlite3 as sq


def sql_start():
    global base, cursor
    base = sq.connect('bot_db.db')
    cursor = base.cursor()
    if base:
        print('Подключение к базе данных - ОК!')
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INT PRIMARY KEY NOT NULL,
        currency VARCHAR(10) DEFAULT usdt)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS records(
        record_id INT PRIMARY KEY,
        user_id INT NOT NULL,
        min_price REAL(20, 2),
        max_price REAL(20, 2),
        FOREIGN KEY (user_id)  REFERENCES users (user_id))""")
    base.commit()