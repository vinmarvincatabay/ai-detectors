# utils.py
import PyPDF2
from docx import Document
import re
import textdistance
import requests

# --- File extraction ---
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

def split_sentences(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if s.strip()]

# --- AI Detection (enhanced heuristics + stylometry) ---
def simple_ai_score(text):
    sentences = split_sentences(text)
    score = 0
    reasons = []

    for s in sentences:
        s_score = 0
        words = s.split()
        if len(words) > 20:
            s_score += 0.15
            reasons.append(f"Long sentence ({len(words)} words)")
        if s.count(',') > 3:
            s_score += 0.1
            reasons.append("Many commas")
        if len(set(words)) / len(words) < 0.6:
            s_score += 0.2
            reasons.append("Repeated words")
        if s.isascii() and any(char.isdigit() for char in s):
            s_score += 0.05
            reasons.append("Contains numbers")
        score += s_score

    score = min(score / len(sentences), 1.0) if sentences else 0
    return score, list(set(reasons))

# --- Similarity Checker (Google API or basic) ---
def check_similarity(sentence, top_k=1):
    api_key = "YOUR_GOOGLE_API_KEY"  # Palitan ng valid key
    cx = "YOUR_SEARCH_ENGINE_ID"     # Palitan ng custom search ID
    sources = []
    try:
        url = f"https://www.googleapis.com/customsearch/v1?q={sentence}&key={api_key}&cx={cx}"
        resp = requests.get(url).json()
        for item in resp.get('items', [])[:top_k]:
            sources.append({'title': item['title'], 'link': item['link']})
    except Exception as e:
        print("API error:", e)
    return sources

# Optional: Simple similarity using textdistance
def sentence_similarity(a, b):
    return textdistance.cosine.normalized_similarity(a, b)
