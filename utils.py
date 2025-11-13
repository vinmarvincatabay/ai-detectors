# utils.py
import sqlite3
from datetime import datetime, timedelta
from io import BytesIO
from docx import Document
import PyPDF2
import os

DB = os.environ.get("AI_DETECTOR_DB", "users.db")

# --- Database helpers ---
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        name TEXT,
        email TEXT,
        password_hash TEXT,
        subscription_expiry TEXT
    )""")
    conn.commit()
    conn.close()

def create_user(username, name, email, password_hash):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO users (username,name,email,password_hash,subscription_expiry) VALUES (?,?,?,?,?)",
              (username, name, email, password_hash, None))
    conn.commit()
    conn.close()

def get_user(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT username,name,email,subscription_expiry FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return
