import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# USERS TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    password TEXT
)
''')

# APPLICATIONS TABLE
cursor.execute('''
CREATE TABLE IF NOT EXISTS applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    phone TEXT,
    qualification TEXT,
    branch TEXT,
    cgpa TEXT,
    job TEXT,
    resume TEXT
)
''')

conn.commit()
conn.close()

print("Database created successfully ✅")