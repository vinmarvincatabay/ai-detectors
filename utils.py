# utils.py

import sqlite3
from datetime import datetime
from io import BytesIO
from docx import Document
import PyPDF2
import textdistance
import os

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

def extract_text_from_uploaded(uploaded_file):
    text = ""
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text()
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
    else:
        text = str(uploaded_file.read(), "utf-8")
    return text

def simple_ai_score(text):
    score = 0.0
    reasons = []
    if len(text.split()) > 100:  # example heuristic
        score += 0.3
        reasons.append("Long text")
    return min(score, 1.0), reasons

def similarity_percentage(text1, text2):
    return textdistance.jaccard(text1, text2)

def get_user(username):
    pass

def check_subscription_active(username):
    return True
