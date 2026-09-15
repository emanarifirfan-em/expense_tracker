"Db or tables create krne k liye or tables bnany k liye yh file hai"

import sqlite3

# Step 1: Database sy connect krn k liye
conn = sqlite3.connect('app.db')
cur = conn.cursor()

# Step 2: users table / users k account data 
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Step 3: expenses table / users k expenses input list
cur.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        note TEXT,
        date TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
''')

conn.commit() #changes save krn k liye

#connection band krn k liye
conn.close()

print("Database ready!")
