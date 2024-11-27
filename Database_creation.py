import sqlite3

def create_database():
    """Initializes the SQLite database and creates tables."""
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

    cursor.execute("""INSERT INTO USERS (username, password, first_name, last_name, age, address, gender, marital_status, wallet)
                      VALUES ('johndoe', 'password123', 'John', 'Doe', 30, '123 Main St', 'Male', 'Single', 50)""")
    cursor.execute("""INSERT INTO USERS (username, password, first_name, last_name, age, address, gender, marital_status, wallet)
                      VALUES ('janedoe', 'securepassword', 'Jane', 'Doe', 28, '456 Elm St', 'Female', 'Married', 100)""")

    conn.commit()
    conn.close()
    print("Database and USERS table created successfully with sample data.")

if __name__ == "__main__":
    create_database()
