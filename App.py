import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Tampilan & CSS (Mempercantik Desain)
st.set_page_config(page_title="AI Paraphraser", page_icon="📝", layout="centered")

st.markdown("""
    <style>
    /* Mengubah font dan warna background utama */
    .main {
        background-color: #0f1116;
    }
    /* Mempercantik tombol agar terlihat modern */
    div.stButton > button:first-child {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        width: 100%;
        height: 3em;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #0056b3;
        border: none;
    }
    /* Mempercantik area input */
    .stTextArea textarea {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Ambil API Key dari Secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("API Key tidak ditemukan di Secrets!")

st.title("📝 AI Paraphraser")

user_text = st.text_area("Masukkan teks:", height=150)

if st.button("Proses"):
    if user_text:
        with st.spinner("Tunggu sebentar..."):
            try:
                # Pastikan nama model ini benar
                model = genai.GenerativeModel("gemini-flash-lite-latest")
                response = model.generate_content(f"Parafrase teks ini: {user_text}")
                
                st.success("Hasil:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Isi teks dulu!")

st.markdown("---")
st.caption("Developed by Reno Ryan Saputra | Built with Vibe Coding ⚡")
