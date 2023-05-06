import sqlite3
import sqlite3 as sq


# def sql_start():
#     global base, cursor
#     base = sq.connect('bot_db.db')
#     cursor = base.cursor()
#     if base:
#         print('Подключение к базе данных - ОК!')
#     cursor.execute("""CREATE TABLE IF NOT EXISTS users(
#         id INT PRIMARY KEY,
#         user_id INT NOT NULL,
#         currency VARCHAR(10) DEFAULT usdt)""")
#     cursor.execute("""CREATE TABLE IF NOT EXISTS records(
#         record_id INT PRIMARY KEY,
#         user_id INT NOT NULL,
#         min_price REAL(20, 2),
#         max_price REAL(20, 2),
#         FOREIGN KEY (user_id)  REFERENCES users (user_id))""")
#     base.commit()

class BotDB:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        if self.conn:
            print('Подключение к базе данных - ОК!')
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id INT PRIMARY KEY NOT NULL, currency VARCHAR(10) DEFAULT usdt)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS records(record_id INT PRIMARY KEY, user_id INT NOT NULL, min_price REAL(20, 2), max_price REAL(20, 2), FOREIGN KEY (user_id)  REFERENCES users (user_id))")
        self.conn.commit()

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def add_user(self, user_id):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        return self.conn.commit()

    def get_user(self, user_id):
        result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return result.fetchall()[0]

    def get_currency(self, user_id):
        result = self.cursor.execute("SELECT currency FROM users WHERE user_id = ?", (user_id,))
        return result.fetchone()[0]

    def update_currency(self, user_id, currency):
        self.cursor.execute("UPDATE users SET currency = ? WHERE user_id = ?", (currency, user_id))
        return self.conn.commit()

    def borders_exists(self, user_id):
        result = self.cursor.execute("SELECT * FROM records WHERE user_id = ?", (user_id,))
        return bool(len(result.fetchall()))

    def get_borders(self, user_id):
        result = self.cursor.execute("SELECT min_price, max_price FROM records WHERE user_id = ?", (user_id,))
        return result.fetchone()

    def set_min_price(self, user_id, min_price):
        self.cursor.execute("UPDATE records SET min_price = ? WHERE user_id = ?", (min_price, user_id))
        return self.conn.commit()

    def set_max_price(self, user_id, max_price):
        self.cursor.execute("UPDATE records SET max_price = ? WHERE user_id = ?", (max_price, user_id))
        return self.conn.commit()

