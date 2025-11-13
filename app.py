# app.py
import streamlit as st
from utils import extract_text_from_uploaded, split_sentences, simple_ai_score, check_similarity, sentence_similarity

st.set_page_config(page_title="Filipino AI + Similarity Checker", layout="wide")
st.title("🇵🇭 Filipino AI Detector & Similarity Checker")

uploaded_file = st.file_uploader("I-upload ang .txt, .docx, o .pdf file", type=["txt","docx","pdf"])

if uploaded_file:
    text = extract_text_from_uploaded(uploaded_file)
    st.subheader("📄 Preview (unang 2000 characters)")
    st.write(text[:2000])

    # --- AI Detection ---
    ai_score, reasons = simple_ai_score(text)
    st.metric("AI-likelihood", f"{int(ai_score*100)}%")
    if reasons:
        st.write("Indicators found:", reasons)

    # --- Similarity Check ---
    st.subheader("🔍 Similarity / Source Highlighting")
    sentences = split_sentences(text)
    for s in sentences:
        sources = check_similarity(s)
        sim_text = f"**{s}**"
        if sources:
            st.markdown(f"{sim_text} → Similar content found at:")
            for src in sources:
                st.markdown(f"- [{src['title']}]({src['link']})")
        else:
            st.write(s)
