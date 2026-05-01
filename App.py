import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Tampilan Awal
st.set_page_config(page_title="Paraphraser Bre AI", page_icon="✨", layout="wide")

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
    icon = "☀️ Mode Terang"
else:
    bg_color = "#f8f9fa" 
    text_color = "#1f2937"
    card_bg = "#ffffff"
    icon = "🌙 Mode Gelap"

# --- SIDEBAR / HEADER ---
col_title, col_theme = st.columns([8, 2])
with col_title:
    st.title("✨ Paraphraser Bre AI")
    st.markdown("**Solusi cerdas menurunkan skor plagiasi & merapikan struktur kalimat.**")
with col_theme:
    st.write("") # Spacing
    if st.button(icon, use_container_width=True):
        toggle_theme()
        st.rerun()

st.divider()

# --- INPUT TEKS & PENGATURAN ---
col_input, col_settings = st.columns([2, 1])

with col_input:
    user_text = st.text_area("Teks Asli:", placeholder="Tempel naskah skripsi, jurnal, atau artikel Anda di sini...", height=320)

with col_settings:
    st.subheader("⚙️ Custom Mode")
    
    # Bungkus pengaturan dalam kartu (container)
    with st.container():
        mode = st.selectbox("Gaya Bahasa (Tone):", [
            "Akademik Formal (Standar Jurnal)", 
            "Formal Analitis (Fokus KKO & Baku)", 
            "Santai (Artikel Blog)", 
            "Ringkas (Padat & Jelas)"
        ])
        
        # Slider Intensitas (Spasinya disejajarkan dengan mode)
        level = st.select_slider(
            "Intensitas Perubahan AI:", 
            options=["Rendah", "Sedang", "Tinggi"],
            value="Sedang"
        )

    # Menentukan warna teks dan pergeseran warna (Hue-Rotate)
        if level == "Rendah":
            slider_color = "#FF4B4B"  # Warna teks Merah
            hue_deg = "0deg"          # Garis tetap merah
        elif level == "Sedang":
            slider_color = "#FF9500"  # Warna teks Oranye
            hue_deg = "40deg"         # Garis diputar ke oranye
        else:
            slider_color = "#34C759"  # Warna teks Hijau
            hue_deg = "120deg"        # Garis diputar ke hijau

        # Menggunakan expander agar UI tidak terlalu penuh
        with st.expander("📌 Lihat Fitur Utama"):
            st.markdown("""
            - 🛡️ **Anti-AI Detector Tuning**
            - 🔄 **Variasi Sintaksis Radikal**
            - 📉 **Penurunan Skor Plagiasi**
            """)

# --- CSS CUSTOM ---
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}

    /* ========================================= */
    /* 1. SENJATA PAMUNGKAS: HAPUS TICKMARK & TEKS */
    /* ========================================= */
    
    /* Menghapus seluruh kontainer teks (Rendah/Sedang/Tinggi) di bawah slider */
    div[data-testid="stTickBar"],
    div[data-testid="stSliderTickBar"] {{
        display: none !important;
    }}

    /* Menghapus titik-titik penanda (marks) kecil di sepanjang garis slider */
    .stSlider [data-baseweb="slider"] ul,
    .stSlider [data-baseweb="slider"] li {{
        display: none !important;
    }}

    /* Menutup celah kosong yang ditinggalkan oleh teks di bawah */
    .stSlider [data-baseweb="slider"] + div + div {{
        display: none !important;
    }}


  /* ========================================= */
    /* 2. TRIK HUE-ROTATE (GARIS & TITIK SUPER RAPI) */
    /* ========================================= */
    /* Kita tidak menimpa background agar persentase garis tidak bocor, 
       melainkan kita "putar" spektrum warnanya secara halus */
 /* Contoh menggabungkan putaran warna dengan peningkat kecerahan */
    .stSlider [data-baseweb="slider"] > div {{
        filter: hue-rotate({hue_deg}) brightness(1.5); 
        transition: filter 0.4s ease-in-out;
    }}

    /* Mempercantik titik bulat (Thumb) */
    .stSlider [role="slider"] {{
        border: 3px solid #ffffff !important; 
        box-shadow: 0 3px 8px rgba(0,0,0,0.3) !important; 
        width: 24px !important; 
        height: 24px !important;
        transition: transform 0.2s !important;
        /* Background-color tidak perlu disetting, otomatis ikut hue-rotate parent */
    }}
    
    .stSlider [role="slider"]:active {{
        transform: scale(1.15); 
    }}

    /* ========================================= */
    /* 3. TEKS INDIKATOR AKTIF DI ATAS TITIK */
    /* ========================================= */
    .stSlider [data-baseweb="slider"] + div{{
        color: {slider_color} !important;
        font-weight: 800 !important;
        font-size: 1.15rem !important;
        letter-spacing: 0.5px;
        transition: color 0.4s ease-in-out;
    }}
    /* TOMBOL GASS KEUNN PREMIUM */
    .stButton>button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-radius: 12px;
        border: none;
        padding: 10px 24px;
        font-weight: 800;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    .stButton>button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }}

   /* 6. Perbaikan Warna Label Widget (Sapu Jagat) */
    label, 
    label p, 
    label span, 
    div[data-testid="stWidgetLabel"] p,
    div[data-testid="stWidgetLabel"] span {{
        color: {text_color} !important;
        font-weight: bold !important;
        transition: color 0.3s ease;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- EKSEKUSI ---
st.write("")
if st.button("🚀 Gass Keunn", use_container_width=True):
    if user_text:
        with st.spinner("Mohon bersabar bukan ujian... 😝"):
            try:
                # Konfigurasi AI
                API_KEY = st.secrets["GEMINI_API_KEY"]
                genai.configure(api_key=API_KEY)
                # Perbaikan kecil pada nama model agar pasti jalan
                model = genai.GenerativeModel("gemini-flash-latest")
                
           # 1. LOGIKA PROMPT DINAMIS BERDASARKAN SLIDER
                if level == "Rendah":
                    instruksi_level = """
                    - Lakukan parafrase RINGAN. 
                    - Fokus HANYA pada penggantian sinonim kata dasar (sekitar 20-30% teks). 
                    - PERTAHANKAN struktur kalimat asli, susunan paragraf, dan panjang teks.
                    - TUJUAN: Teks persis seperti asli tapi bisa lolos cek plagiasi dasar.
                    """
                elif level == "Sedang":
                    instruksi_level = """
                    - Lakukan parafrase MENENGAH. 
                    - Ganti sinonim kata dan susun ulang urutan klausa (misal: kalimat aktif menjadi pasif). 
                    - TUJUAN: Teks mengalir lebih luwes, enak dibaca, namun kerangka pemikirannya tetap utuh seperti aslinya.
                    """
                else: # Tinggi
                    instruksi_level = """
                    - Lakukan parafrase MENDALAM. 
                    - Rombak struktur paragraf dan kalimat secara menyeluruh tanpa mengubah makna aslinya. 
                    - TUJUAN: Teks terlihat seperti ditulis ulang sepenuhnya oleh penulis yang berbeda dengan gaya bahasa yang segar.
                    """

                # 2. MASTER PROMPT (ANTI SOK PINTAR)
                refined_prompt = f"""
                Bertindaklah sebagai Editor Profesional. 
                Tugas Anda adalah memparafrase teks di bawah ini dengan gaya bahasa: {mode}.

                TINGKAT INTENSITAS PARAFRASE: {level}
                INSTRUKSI UNTUK INTENSITAS INI:
                {instruksi_level}

                ATURAN MUTLAK (WAJIB DIPATUHI):
                1. KETERBACAAN (READABILITY) ADALAH RAJA: Gunakan bahasa Indonesia yang baku, logis, namun TETAP SANGAT MUDAH DIPAHAMI oleh pembaca umum.
                2. DILARANG MENGGUNAKAN KATA SULIT/FILOSOFIS: Dilarang keras menggunakan istilah yang kaku, aneh, atau jarang dipakai (contoh yang HARUS DIHINDARI: "resiprokal", "orkestrasi", "aksidental", "persistensi", "instrumentasi", "dikotomi"). Gunakan kosakata yang umum dijumpai dalam jurnal penelitian standar.
                3. ANTI-ROBOTIK: Buat transisi antar kalimat yang mengalir layaknya ditulis oleh manusia. Jangan gunakan kata penghubung klise khas AI (contoh hindari: "penting untuk diingat", "dalam kesimpulannya", "di sisi lain").
                4. LUGAS DAN PADAT: Jangan bertele-tele atau menambahkan opini baru.
                
                Teks Asli: 
                {user_text}
                """
                
                response = model.generate_content(refined_prompt)
                
                # Menampilkan notifikasi sukses kecil di pojok
                st.toast('Selesai! Teks berhasil dioptimasi 🎉', icon='✅')
                
                st.divider()
                st.subheader("📊 Hasil Analisis & Perbandingan")
                
                # FITUR BARU: Menghitung jumlah kata
                word_count_asli = len(user_text.split())
                word_count_hasil = len(response.text.split())
                
                # Menampilkan Metrik
                col_met1, col_met2, col_met3 = st.columns(3)
                col_met1.metric(label="Jumlah Kata Asli", value=word_count_asli)
                col_met2.metric(label="Jumlah Kata Hasil", value=word_count_hasil, delta=word_count_hasil - word_count_asli)
                col_met3.metric(label="Status Optimasi", value="Aman 🛡️")
                
                st.write("---")
                
                # Menampilkan Teks
                col_res1, col_res2 = st.columns(2)
                with col_res1:
                    st.caption("Teks Asli")
                    st.info(user_text)
                with col_res2:
                    st.caption("Hasil Optimasi AI")
                    st.success(response.text)
                    
                st.write("---")
                
                # FITUR BARU: Tombol Download & Copy
                col_copy, col_down = st.columns(2)
                with col_copy:
                    st.subheader("📋 Salin Hasil:")
                    st.code(response.text, language=None)
                with col_down:
                    st.subheader("💾 Simpan File:")
                    st.write("Unduh hasil parafrase dalam bentuk file Teks.")
                    st.download_button(
                        label="Download Hasil (.txt)",
                        data=response.text,
                        file_name="Hasil_Parafrase_AI.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
            except Exception as e:
                st.error(f"Terjadi kendala teknis: {e}")
    else:
        st.warning("Silakan masukkan naskah Anda terlebih dahulu! 📝")

# Footer
st.divider()
st.markdown("<p style='text-align: center; color: gray;'>Developed with AI by Reno Ryan Saputra</p>", unsafe_allow_html=True)
