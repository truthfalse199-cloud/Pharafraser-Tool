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

# 2. Ambil API Key dari Secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("Waduh, API Key belum terpasang di Secrets Streamlit!")

# 3. Header Website
st.title("📝 AI Paraphraser Pro")
st.markdown("---")

# 4. Input Teks
user_text = st.text_area("Masukkan Kalimat Asli:", placeholder="Tempel naskah skripsi Anda di sini...", height=200)

# 5. Pilihan Gaya Bahasa (Horizontal)
col1, col2 = st.columns(2)
with col1:
    mode = st.selectbox("Gaya Bahasa:", ["Akademik (Baku)", "Standar", "Santai"])
with col2:
    target = st.selectbox("Tujuan:", ["Munaqasyah", "Publikasi Jurnal", "Tugas Harian"])

# 6. Proses Parafrase
if st.button("🚀 Mulai Parafrase"):
    if user_text:
        with st.spinner("Sedang memproses kata-kata..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                # Prompt yang lebih spesifik untuk hasil maksimal
                prompt = f"Anda adalah editor jurnal ilmiah. Lakukan parafrase pada teks berikut dengan gaya {mode} untuk keperluan {target}. Pastikan kosakata yang dihasilkan variatif, formal, dan mempertahankan makna asli: {user_text}"
                
                response = model.generate_content(prompt)
                
                st.success("Selesai! Berikut hasilnya:")
                st.write(response.text)
                
                # Fitur tambahan: Salin teks (Copy to Clipboard)
                st.code(response.text, language=None)
                
            except Exception as e:
                st.error(f"Error saat menghubungi AI: {e}")
    else:
        st.warning("Masukkan teks dulu ya!")

st.markdown("---")
st.caption("Developed by Reno Ryan Saputra | Built with Vibe Coding ⚡")
