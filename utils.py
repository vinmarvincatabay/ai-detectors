# utils.py
import sqlite3
from datetime import datetime, timedelta
from io import BytesIO
from docx import Document
import PyPDF2
import os
import textdistance

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

def get_user(username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT username,name,email,subscription_expiry FROM users WHERE username=?", (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return {"username": row[0], "name": row[1], "email": row[2], "subscription_expiry": row[3]}

def check_subscription_active(username):
    user = get_user(username)
    if not user or not user.get("subscription_expiry"):
        return False, None
    expiry = datetime.fromisoformat(user["subscription_expiry"])
    return (expiry >= datetime.utcnow()), user["subscription_expiry"]

# --- File text extraction ---
def extract_text_from_uploaded(uploaded_file):
    name = uploaded_file.name.lower()
    data = uploaded_file.getvalue()
    if name.endswith(".txt"):
        return data.decode("utf-8", errors="ignore")
    elif name.endswith(".docx"):
        doc = Document(BytesIO(data))
        return "\n".join([p.text for p in doc.paragraphs])
    elif name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(BytesIO(data))
        text = []
        for p in reader.pages:
            text.append(p.extract_text() or "")
        return "\n".join(text)
    else:
        return ""

# --- Simple AI-likelihood scorer (rule-based) ---
def simple_ai_score(text):
    indicators = [
        "sa pangkalahatan", "bilang konklusyon", "ayon sa pananaliksik",
        "ipinapakita ng datos", "sa kabuuan", "sa madaling sabi", "sa kabuuan ng",
        "maaaring", "mga sumusunod"
    ]
    text_low = text.lower()
    found = [k for k in indicators if k in text_low]
    count = len(found)
    score = min(1.0, 0.2 * count)  # Maximum 100%
    return score, found

# --- Similarity checker ---
def similarity_percentage(text1, text2):
    sim = textdistance.jaccard.similarity(text1, text2)
    return sim
