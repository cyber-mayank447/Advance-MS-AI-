import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "jarvis.db")
con = sqlite3.connect(DB_PATH)
cursor = con.cursor()

# Required tables for the MS UI and command manager.
cursor.execute("""
CREATE TABLE IF NOT EXISTS sys_command (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    path VARCHAR(1000) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS web_command (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    url VARCHAR(1000) NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    mobile_no VARCHAR(255),
    email VARCHAR(255),
    address VARCHAR(255)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100),
    designation VARCHAR(50),
    mobileno VARCHAR(40),
    email VARCHAR(200),
    city VARCHAR(300)
)
""")

# Useful default web commands. INSERT OR IGNORE prevents duplicates.
defaults = [
    ("youtube", "https://www.youtube.com/"),
    ("google", "https://www.google.com/"),
    ("github", "https://github.com/"),
    ("whatsapp", "https://web.whatsapp.com/"),
]
for name, url in defaults:
    cursor.execute(
        "INSERT OR IGNORE INTO web_command (name, url) VALUES (?, ?)",
        (name, url)
    )

con.commit()

def get_connection():
    return sqlite3.connect(DB_PATH)

def close():
    con.commit()
    con.close()
