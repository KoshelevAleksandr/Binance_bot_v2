import sqlite3

try:
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id INT PRIMARY KEY NOT NULL, currency VARCHAR(10) DEFAULT usdt)")
    cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (1000,))

    users = cursor.execute("SELECT * FROM 'users'")
    print(users.fetchall())

    conn.commit()

except sqlite3.Error as error:
    print("Error", error)

finally:
    if(conn):
        conn.close()


