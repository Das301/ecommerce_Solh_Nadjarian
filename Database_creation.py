import sqlite3

conn = sqlite3.connect('eCommerce.db')
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE if not exists USERS (
               id INT PRIMARY KEY,
               username TEXT UNIQUE NOT NULL,
               password TEXT NOT NULL,
               first_name TEXT NOT NULL,
               last_name TEXT NOT NULL,
               age INT NOT NULL,
               address TEXT NOT NULL,
               gender TEXT NOT NULL,
               marital_status TEXT NOT NULL,
               wallet REAL DEFAULT 0)""")

cursor.execute("""CREATE TABLE if not exists GOODS (
               id INT PRIMARY KEY,
               name TEXT NOT NULL UNIQUE,
               description TEXT NOT NULL,
               price REAL NOT NULL,
               category TEXT NOT NULL,
               stocks INT NOT NULL DEFAULT 0)""")

cursor.execute("""CREATE TABLE if not exists PURCHASES (
               id INT PRIMARY KEY,
               user TEXT NOT NULL,
               good TEXT NOT NULL,
               quantity INT NOT NULL,
               total_price REAL NOT NULL,
               FOREIGN KEY (user) REFERENCES USERS(username),
               FOREIGN KEY (good) REFERENCES GOODS(name))""")

cursor.execute("""CREATE TABLE if not exists REVIEWS (
               id INT PRIMARY KEY,
               user TEXT NOT NULL,
               good TEXT NOT NULL,
               review TEXT NOT NULL,
               FOREIGN KEY (user) REFERENCES USERS(username),
               FOREIGN KEY (good) REFERENCES GOODS(name))""")

conn.commit()
