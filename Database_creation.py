import sqlite3

conn = sqlite3.connect('eCommerce.db')
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE if not exists USERS (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
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
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL UNIQUE,
               description TEXT NOT NULL,
               price REAL NOT NULL,
               category TEXT NOT NULL,
               stocks INT NOT NULL DEFAULT 0)""")

cursor.execute("""CREATE TABLE if not exists PURCHASES (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user TEXT NOT NULL,
               good TEXT NOT NULL,
               quantity INT NOT NULL,
               total_price REAL NOT NULL,
               FOREIGN KEY (user) REFERENCES USERS(username),
               FOREIGN KEY (good) REFERENCES GOODS(name))""")

cursor.execute("""CREATE TABLE if not exists REVIEWS (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user TEXT NOT NULL,
               good TEXT NOT NULL,
               review TEXT NOT NULL,
               rating REAL NOT NULL CHECK (rating>=0 AND rating<=10),
               flag INTEGET NOT NULL DEFAULT 0 CHECK(flag=0 OR flag=1),
               FOREIGN KEY (user) REFERENCES USERS(username),
               FOREIGN KEY (good) REFERENCES GOODS(name))""")

cursor.execute("""CREATE TABLE if not exists ADMINS (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT UNIQUE NOT NULL,
               password TEXT NOT NULL,
               first_name TEXT NOT NULL,
               last_name TEXT NOT NULL,
               age INT NOT NULL,
               address TEXT NOT NULL)""")

conn.commit()

cursor.execute("INSERT INTO ADMINS (username, password, first_name, last_name, age, address) VALUES ('Das35', '24h_D@yt0n@', 'Dany', 'Solh', 21, 'Beirut, Lebanon')")
cursor.execute("INSERT INTO GOODS(name, description, price, category, stocks) VALUES ('Michelin Soft Sports Tires', 'A set of 4 Michelin soft sports tires, ideal for occasional track days', 600, 'Tire', 10)")
cursor.execute("INSERT INTO USERS (username, password, first_name, last_name, age, address, gender, marital_status, wallet) VALUES ('DanySolh21', '24h_LeM@ns', 'Dany', 'Solh', 21, 'Beirut, Lebanon', 'Male', 'Single', 1400)")
cursor.execute("INSERT INTO GOODS(name, description, price, category, stocks) VALUES('Lug Nuts', 'A set of 20 lug nuts for a variety of tires', 20, 'Tires', 5)")
conn.commit()

