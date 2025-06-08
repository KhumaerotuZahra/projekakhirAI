import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API key dari .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openai/gpt-3.5-turbo"

# Fungsi untuk analisis sentimen menggunakan GPT
def analyze_sentiment_gpt(text):
    messages = [
        {"role": "system", "content": "Kamu adalah asisten analisis sentimen yang hanya boleh membalas dengan kata 'Positif', 'Negatif', atau 'Netral', tanpa penjelasan tambahan."},
        {"role": "user", "content": f"Tolong analisis sentimen dari kalimat ini:\n{text}"}
    ]
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": messages,
                "temperature": 0,
                "max_tokens": 10
            }
        )
        response.raise_for_status()
        result = response.json()
        sentiment = result['choices'][0]['message']['content'].strip().capitalize()
        if sentiment not in ['Positif', 'Negatif', 'Netral']:
            sentiment = "Tidak dapat menentukan sentimen"
        return sentiment
    except Exception as e:
        return f"Error: {e}"

# ===== UI Streamlit =====
st.markdown(
    """
    <h1 style='text-align: center; color: #333;'>🧠 Analisis Sentimen</h1>
    <hr style="border:1px solid #eee"/>
    """,
    unsafe_allow_html=True
)

user_input = st.text_area("✍️ Masukkan kalimat untuk dianalisis:")

if st.button("🔍 Analisis"):
    if user_input.strip() == "":
        st.warning("⚠️ Mohon masukkan teks terlebih dahulu.")
    else:
        with st.spinner("⏳ Sedang menganalisis..."):
            hasil = analyze_sentiment_gpt(user_input)
            st.success(f"**Hasil Sentimen:** {hasil}")

st.markdown(
    """
    <div style='position: fixed; bottom: 10px; right: 10px; font-size: 12px; color: #555; background-color: rgba(255, 255, 255, 0.6); padding: 4px 8px; border-radius: 5px; box-shadow: 0 0 5px rgba(0,0,0,0.1);'>
        Bantuan ChatGPT
    </div>
    """,
    unsafe_allow_html=True
)
