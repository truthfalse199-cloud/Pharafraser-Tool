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
    icon = "☀️"  # Tampilkan matahari saat mode gelap (untuk ganti ke terang)
else:
    bg_color = "#ffffff"
    text_color = "#000000"
    card_bg = "#f0f2f6"
    icon = "🌙"  # Tampilkan bulan saat mode terang (untuk ganti ke gelap)

# --- CSS CUSTOM (Termasuk Posisi Ikon di Pojok Kanan) ---
st.markdown(f"""
   <style>
   <style>
   /* Mengubah warna garis (track) yang sudah dilewati slider */
    .stSlider [data-baseweb="slider"] > div > div {{
        background: {slider_color} !important;
    }}

    /* Mengubah warna bulatan (thumb) slider */
    .stSlider [role="slider"] {{
        background-color: {slider_color} !important;
        border: 2px solid {slider_color};
    }}

    /* Mengubah warna teks label saat digeser */
    .stSlider [data-testid="stWidgetLabel"] p {{
        color: {text_color};
    }}
    slider_color = "#ff4b4b" # Default Merah
if level == "Sedang":
    slider_color = "#ffeb3b" # Kuning
elif level == "Tinggi":
    slider_color = "#4caf50" # Hijau
    /* Mengubah warna background seluruh aplikasi */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    
    /* MEMPERBAIKI WARNA LABEL (Teks di atas input/slider) */
    .stWidgetLabel p {{
        color: {text_color} !important;
        font-weight: bold;
    }}

    /* MEMPERBAIKI TEKS DI DALAM SELECTBOX */
    div[data-baseweb="select"] > div {{
        background-color: {card_bg};
        color: {text_color};
    }}

    /* MEMPERBAIKI TEKS DI DALAM TEXT AREA */
    .stTextArea textarea {{
        background-color: {card_bg};
        color: {text_color};
        border-radius: 10px;
    }}

    /* TOMBOL PROSES */
    .stButton>button {{
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        font-weight: bold;
        background-color: #007bff;
        color: white;
        border: none;
    }}
    </style>
    """, unsafe_allow_html=True)

# Tombol Ganti Tema (Terletak di pojok kanan)
with st.container():
    col_empty, col_theme = st.columns([10, 1])
    with col_theme:
        if st.button(icon):
            toggle_theme()
            st.rerun()

# 2. Inisialisasi AI
try:
    # Menggunakan Secrets Streamlit untuk keamanan
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("API Key tidak ditemukan. Pastikan sudah input di menu Secrets!")

# 3. Header
st.title("📝 Parafrase AI")
st.write("Gunakan AI untuk menurunkan skor plagiasi dan memperbaiki struktur kalimat secara profesional.")
st.divider()

# 4. Input Teks & Pengaturan
col_input, col_settings = st.columns([2, 1])

with col_input:
    user_text = st.text_area("Teks Asli:", placeholder="Tempel naskah skripsi atau jurnal Anda di sini...", height=300)

with col_settings:
    st.subheader("⚙️ Costum Mode")
    mode = st.selectbox("Gaya Bahasa (Tone):", [
        "Akademik Formal (Standar Jurnal)", 
        "Mode Munaqasyah (Fokus KKO & Baku)", 
        "Santai (Artikel Blog)", 
        "Ringkas (Padat & Jelas)"
    ])
    
    level = st.select_slider("Intensitas Perubahan:", options=["Rendah", "Sedang", "Tinggi"])
    
    st.info("""
    **Fitur Utama:**
    - Anti-AI Detector Tuning
    - Variasi Sintaksis Radikal
    - Penurunan Skor Plagiasi
    """)

# 5. Eksekusi dengan Prompt Baru
if st.button("Gass Keunn 🚀"):
    if user_text:
        with st.spinner("Harap bersabar Bukan Ujian 😝..."):
            try:
                # Menggunakan model yang sudah berhasil Anda coba sebelumnya
                model = genai.GenerativeModel("gemini-flash-lite-latest")
                
                # Integrasi Prompt Premium Anda yang sudah diperbagus
                refined_prompt = f"""
                Bertindaklah sebagai Editor Akademik Senior dan Ahli Linguistik. 
                Tugas Anda adalah menulis ulang teks di bawah ini dengan gaya {mode} dan tingkat perubahan {level}.

                TUJUAN UTAMA: Menurunkan skor plagiasi dan melewati deteksi AI Writer dengan cara:
                1. VARIASI SINTAKSIS: Ubah struktur kalimat secara radikal (misal: aktif ke pasif, atau mengubah urutan klausa) tanpa mengubah esensi makna.
                2. BURSTINESS: Campurkan kalimat pendek yang tegas dengan kalimat kompleks yang mengalir untuk meniru pola tulisan manusia.
                3. DIKSI SPESIFIK: Gunakan sinonim kontekstual. Hindari kata klise AI seperti 'esensial', 'mendalam', atau 'signifikan'.
                4. ANTI-THESIS: Hindari struktur perbandingan yang terlalu simetris/robotik. Buat alur argumen yang organik.
                5. HUMAN-LIKE FLOW: Pastikan transisi antar kalimat tidak kaku.
                
                Teks yang harus diparafrase:
                {user_text}
                """
                
                response = model.generate_content(refined_prompt)
                
                st.divider()
                
                # 6. Hasil & Perbandingan
                st.subheader("📊 Hasil Perbandingan")
                col_res1, col_res2 = st.columns(2)
                
                with col_res1:
                    st.caption("Teks Asli")
                    st.write(user_text)
                
                with col_res2:
                    st.caption("Hasil Optimasi AI")
                    st.write(response.text)
                    
                st.write("---")
                st.subheader("📋 Salin Hasil Final:")
                st.code(response.text, language=None)
                st.success("Parafrase selesai dengan optimasi anti-plagiasi.")
                
            except Exception as e:
                st.error(f"Terjadi kendala teknis: {e}")
    else:
        st.warning("Silakan masukkan teks terlebih dahulu.")

# Footer
st.divider()
st.caption("Developed by Reno Ryan Saputra ❤️")
