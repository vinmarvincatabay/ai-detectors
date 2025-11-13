# utils.py
import sqlite3
from datetime import datetime
from io import BytesIO
from docx import Document
import PyPDF2
import textdistance
import os

# --- Database helpers ---
def init_db():
    conn = sqlite3.connect("users.db")
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

def get_user(username):
    # ...function code...

def check_subscription_active(username):
    # ...function code...

# --- File text extraction ---
def extract_text_from_uploaded(uploaded_file):
    # ...function code...

# --- Simple AI-likelihood scorer ---
def simple_ai_score(text):
    # ...function code...

# --- Similarity checker ---
def similarity_percentage(text1, text2):
    # ...function code...
