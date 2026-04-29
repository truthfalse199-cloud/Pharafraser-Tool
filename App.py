import streamlit as st
import google.generativeai as genai


# Konfigurasi Tampilan Website
st.set_page_config(page_title="AI Paraphraser", page_icon="📝")

st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    </style>
    """, unsafe_check_markdown=True)

# --- BAGIAN INPUT API KEY ---
# Nanti kita bisa buat lebih aman, tapi untuk awal, masukkan di sini
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)

st.title("📝 AI Academic Paraphraser")
st.subheader("Ubah teks Anda menjadi lebih profesional & natural")

# Input Teks dari User
user_text = st.text_area("Masukkan teks asli di sini:", placeholder="Tempel naskah skripsi atau tulisan Anda...", height=200)

# Pilihan Mode
mode = st.select_slider(
    "Pilih Gaya Bahasa:",
    options=["Santai", "Standar", "Akademik Formal"]
)

if st.button("Proses Parafrase"):
    if user_text:
        with st.spinner("Sedang memproses..."):
            try:
                model = genai.GenerativeModel("gemini-1.5-flash")
                prompt = f"Lakukan parafrase pada teks berikut dengan gaya {mode}. Pastikan maknanya tetap sama namun kosa katanya lebih bervariasi dan profesional untuk keperluan universitas: {user_text}"
                
                response = model.generate_content(prompt)
                
                st.success("Hasil Parafrase:")
                st.write(response.text)
                st.divider()
                st.info("Tips: Selalu periksa kembali hasil parafrase untuk memastikan konteks tetap akurat.")
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")
    else:
        st.warning("Silakan masukkan teks terlebih dahulu!")
