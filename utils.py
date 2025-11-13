# utils.py
import PyPDF2
from docx import Document
import re
import textdistance
from sentence_transformers import SentenceTransformer
import requests

# Load sentence embedding model once
model = SentenceTransformer('all-MiniLM-L6-v2')

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

# --- AI Detection ---
def simple_ai_score(text):
    sentences = split_sentences(text)
    score = 0
    reasons = []

    for s in sentences:
        s_score = 0
        if len(s.split()) > 25:
            s_score += 0.2
            reasons.append("Long sentence")
        if s.count(',') > 3:
            s_score += 0.1
            reasons.append("Many commas")
        if len(set(s.split())) / len(s.split()) < 0.5:
            s_score += 0.2
            reasons.append("Repeated words")
        score += s_score

    score = min(score / len(sentences), 1.0) if sentences else 0
    return score, reasons

# --- Similarity Checker (Google/Bing API) ---
def check_similarity(sentence, top_k=1):
    api_key = "YOUR_GOOGLE_API_KEY"  # Palitan ng key mo
    cx = "YOUR_SEARCH_ENGINE_ID"     # Palitan ng custom search ID mo
    url = f"https://www.googleapis.com/customsearch/v1?q={sentence}&key={api_key}&cx={cx}"
    sources = []
    try:
        resp = requests.get(url).json()
        for item in resp.get('items', [])[:top_k]:
            sources.append({'title': item['title'], 'link': item['link']})
    except Exception as e:
        print("API error:", e)
    return sources
