# app.py
import streamlit as st
from langdetect import detect
import textdistance
from utils import init_db, extract_text_from_uploaded, simple_ai_score, check_subscription_active, get_user
import streamlit_authenticator as stauth

# Initialize DB
init_db()

st.set_page_config(page_title="Filipino AI & Similarity Detector", layout="wide")

# Demo credentials
credentials = {
    "usernames": {
        "demo": {"name": "Demo User", "password": "demo123"}
    }
}

authenticator = stauth.Authenticate(
    credentials,
    cookie_name="ai_detector_cookie",
    key="some_secret_key_here",
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.sidebar.write(f"Welcome, {name}!")
    db_username = username or "demo"
    active, expiry = check_subscription_active(db_username)
    if not active:
        st.warning("Walang active subscription. Paki-renew para magamit ang serbisyo.")
        st.stop()

    st.title("🧠 Filipino AI Detector + Similarity Checker")

    uploaded_file = st.file_uploader("I-upload ang .txt, .docx, o .pdf file", type=["txt", "docx", "pdf"])
    if uploaded_file:
        text = extract_text_from_uploaded(uploaded_file)
        st.subheader("📄 Preview (unang 2000 characters)")
        st.write(text[:2000])

        try:
            lang = detect(text)
            st.write(f"Language detected: `{lang}`")
            if lang not in ["tl", "fil"]:
                st.info("Tandaan: ang teksto ay hindi mukhang Filipino. Maaari pa ring ma-process.")
        except Exception:
            st.write("Hindi matukoy ang wika.")

        score, reasons = simple_ai_score(text)
        st.metric("AI-likelihood (approx)", f"{int(score*100)}%")
        if reasons:
            st.write("Indicators found:", reasons)

        st.subheader("🔍 Similarity Checker")
        other = st.text_area("Ilagay ang ibang teksto para i-compare (paste dito):")
        if st.button("Suriin ang Similarity"):
            if not other.strip():
                st.error("Maglagay ng teksto para ikumpara.")
            else:
                sim = textdistance.jaccard.similarity(text, other)
                st.info(f"Similarity: {sim*100:.2f}%")

    authenticator.logout("Logout", "sidebar")

elif authentication_status == False:
    st.error("Mali ang username/password")
else:
    st.info("Please login")
