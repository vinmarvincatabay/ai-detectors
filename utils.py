import streamlit as st
from langdetect import detect
from utils import extract_text_from_uploaded, simple_ai_score, similarity_percentage

st.title("🧠 Filipino AI Detector + Similarity Checker")

uploaded_file = st.file_uploader("I-upload ang .txt, .docx, o .pdf file", type=["txt", "docx", "pdf"])
if uploaded_file:
    text = extract_text_from_uploaded(uploaded_file)
    st.subheader("📄 Preview (unang 2000 characters)")
    st.write(text[:2000])

    try:
        lang = detect(text)
        st.write(f"Language detected: `{lang}`")
    except Exception:
        st.write("Hindi matukoy ang wika.")

    # AI-likelihood
    score, reasons = simple_ai_score(text)
    st.metric("AI-likelihood (approx)", f"{int(score*100)}%")
    if reasons:
        st.write("Indicators found:", reasons)

    # Similarity Checker
    st.subheader("🔍 Similarity Checker")
    other = st.text_area("Ilagay ang ibang teksto para i-compare (paste dito):")
    if st.button("Suriin ang Similarity"):
        if not other.strip():
            st.error("Maglagay ng teksto para ikumpara.")
        else:
            sim = similarity_percentage(text, other)
            st.info(f"Similarity: {sim*100:.2f}%")
