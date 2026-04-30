import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Tampilan Awal
st.set_page_config(page_title="AI Paraphraser Pro", page_icon="📝", layout="wide")

# --- LOGIKA DARK/LIGHT MODE ---
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

def toggle_theme():
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'

# Penentuan Warna Berdasarkan Tema
if st.session_state.theme == 'dark':
    bg_color = "#0f1116"
    text_color = "#ffffff"
    card_bg = "#1d2129"
    icon = "☀️"
else:
    bg_color = "#ffffff"
    text_color = "#000000"
    card_bg = "#f0f2f6"
    icon = "🌙"

# --- SIDEBAR / HEADER ---
st.title("📝 Parafrase AI")
st.write("Gunakan AI untuk menurunkan skor plagiasi dan memperbaiki struktur kalimat secara profesional.")

# Tombol Ganti Tema (Terletak di pojok kanan)
col_title, col_theme = st.columns([10, 1])
with col_theme:
    if st.button(icon):
        toggle_theme()
        st.rerun()

st.divider()

# --- INPUT TEKS & PENGATURAN ---
col_input, col_settings = st.columns([2, 1])

with col_input:
    user_text = st.text_area("Teks Asli:", placeholder="Tempel naskah skripsi atau jurnal Anda di sini...", height=300)

with col_settings:
    st.subheader("⚙️ Custom Mode")
    mode = st.selectbox("Gaya Bahasa (Tone):", [
        "Akademik Formal (Standar Jurnal)", 
        "Mode Munaqasyah (Fokus KKO & Baku)", 
        "Santai (Artikel Blog)", 
        "Ringkas (Padat & Jelas)"
    ])
    
    # PERBAIKAN: Slider harus didefinisikan SEBELUM variabel slider_color digunakan
    level = st.select_slider("Intensitas Perubahan:", options=["Rendah", "Sedang", "Tinggi"], value="Rendah")

    # Logika Warna Slider
    if level == "Rendah":
        slider_color = "#ff4b4b" # Merah
    elif level == "Sedang":
        slider_color = "#ffeb3b" # Kuning
    elif level == "Tinggi":
        slider_color = "#4caf50" # Hijau

    st.info("""
    **Fitur Utama:**
    - Anti-AI Detector Tuning
    - Variasi Sintaksis Radikal
    - Penurunan Skor Plagiasi
    """)

# --- CSS CUSTOM ---
# Kita masukkan CSS di sini agar variabel slider_color sudah terisi
st.markdown(f"""
    <style>
    /* 1. Background Dasar */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}

    /* 3. WARNA GARIS SLIDER (TRACK) */
    /* Bagian Kiri (Aktif) */
    .stSlider [data-baseweb="slider"] > div > div {{
        background: {slider_color} !important;
    }}
    
    /* Bagian Kanan (Kosong) */
    .stSlider [data-baseweb="slider"] > div {{
        background: rgba(224, 224, 224, 0.5) !important; 
    }}

    /* 4. TITIK SLIDER (THUMB) */
    .stSlider [role="slider"] {{
        background-color: {slider_color} !important;
        border: 2px solid white !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3);
    }}

    /* 5. TEKS INDIKATOR AKTIF DI ATAS TITIK */
    .stSlider div[data-baseweb="slider"] + div {{
        color: {slider_color} !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }}

    /* 6. Perapihan Input Lainnya */
    .stWidgetLabel p {{
        color: {text_color} !important;
        font-weight: bold;
    }}
    </style>
    """, unsafe_allow_html=True)


# --- EKSEKUSI ---
if st.button("Gass Keunn 🚀"):
    if user_text:
        with st.spinner("Harap bersabar Bukan Ujian 😝..."):
            try:
                # Konfigurasi AI
                API_KEY = st.secrets["GEMINI_API_KEY"]
                genai.configure(api_key=API_KEY)
                model = genai.GenerativeModel("gemini-1.5-flash-lite-latest")
                
                refined_prompt = f"""
                Bertindaklah sebagai Editor Akademik Senior dan Ahli Linguistik. 
                Tugas Anda adalah menulis ulang teks di bawah ini dengan gaya {mode} dan tingkat perubahan {level}.

                TUJUAN UTAMA: Menurunkan skor plagiasi dan melewati deteksi AI Writer dengan cara:
                1. VARIASI SINTAKSIS: Ubah struktur kalimat secara radikal (aktif-pasif, urutan klausa).
                2. BURSTINESS: Campurkan kalimat pendek tegas dengan kalimat kompleks mengalir.
                3. DIKSI SPESIFIK: Gunakan sinonim kontekstual, hindari kata klise AI.
                4. ANTI-THESIS: Alur organik, tidak robotik.
                5. HUMAN-LIKE FLOW: Transisi alami.
                
                Teks: {user_text}
                """
                
                response = model.generate_content(refined_prompt)
                
                st.divider()
                st.subheader("📊 Hasil Perbandingan")
                col_res1, col_res2 = st.columns(2)
                
                with col_res1:
                    st.caption("Teks Asli")
                    st.info(user_text)
                
                with col_res2:
                    st.caption("Hasil Optimasi AI")
                    st.success(response.text)
                    
                st.write("---")
                st.subheader("📋 Salin Hasil Final:")
                st.code(response.text, language=None)
                
            except Exception as e:
                st.error(f"Terjadi kendala teknis: {e}")
    else:
        st.warning("Silakan masukkan teks terlebih dahulu.")

st.divider()
st.caption("Developed by Reno Ryan Saputra ❤️")
