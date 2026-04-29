import streamlit as st
import google.generativeai as genai

# 1. Konfigurasi Tampilan
st.set_page_config(page_title="AI Paraphraser Pro", page_icon="📝", layout="wide")

# Custom CSS untuk tampilan lebih bersih
st.markdown("""
    <style>
    .stTextArea textarea { border-radius: 10px; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. Inisialisasi AI
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Pastikan GEMINI_API_KEY sudah terisi di Secrets!")

# 3. Header
st.title("📝 AI Academic Paraphraser")
st.write("Optimasi naskah akademik & skripsi Anda dengan kecerdasan buatan.")
st.divider()

# 4. Input Teks & Pengaturan
col_input, col_settings = st.columns([2, 1])

with col_input:
    user_text = st.text_area("Teks Asli:", placeholder="Tempel naskah Anda di sini...", height=250)

with col_settings:
    st.subheader("Pengaturan Gaya")
    # Fitur Mode Khusus Munaqasyah
    mode = st.selectbox("Pilih Gaya Bahasa:", [
        "Akademik Formal (Standar Jurnal)", 
        "Mode Munaqasyah (Fokus KKO & Baku)", 
        "Santai (Artikel Blog)", 
        "Ringkas (Padat & Jelas)"
    ])
    
    level = st.select_slider("Tingkat Perubahan:", options=["Rendah", "Sedang", "Tinggi"])

# 5. Eksekusi
if st.button("🚀 Proses Parafrase Sekarang"):
    if user_text:
        with st.spinner("Sedang merangkai kata terbaik..."):
            try:
                model = genai.GenerativeModel("gemini-flash-lite-latest")
                
                # Prompt Engineering: Memberi instruksi spesifik berdasarkan pilihan user
                system_prompt = f"Anda adalah editor profesional. Lakukan parafrase pada teks berikut dengan gaya {mode} dan tingkat perubahan {level}. "
                if "Munaqasyah" in mode:
                    system_prompt += "Gunakan Kata Kerja Operasional (KKO) yang baku, hindari kata mubazir, dan pastikan kalimat sangat formal sesuai standar universitas."
                
                response = model.generate_content(f"{system_prompt}\n\nTeks: {user_text}")
                
                st.divider()
                
                # 6. Fitur Perbandingan Berdampingan (Side-by-Side)
                st.subheader("Hasil Analisis & Perbandingan")
                col_res1, col_res2 = st.columns(2)
                
                with col_res1:
                    st.info("Teks Asli")
                    st.write(user_text)
                
                with col_res2:
                    st.success("Hasil Parafrase")
                    st.write(response.text)
                    
                # 7. Fitur Copy to Clipboard (Menggunakan st.code)
                st.write("---")
                st.subheader("Salin Hasil:")
                st.code(response.text, language=None)
                
            except Exception as e:
                st.error(f"Terjadi kendala: {e}")
    else:
        st.warning("Silakan masukkan teks terlebih dahulu.")

# Footer
st.divider()
st.caption(f"Versi 2.0 - Dibuat untuk mendukung riset akademik Reno Ryan Saputra")
