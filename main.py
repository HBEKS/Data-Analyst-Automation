import os
import pandas as pd
import ollama
import streamlit as st
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM 
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# 1. Load Environment Variables
load_dotenv()

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="AI Data Analyst Specialist", page_icon="📊", layout="wide")

# --- FUNGSI HELPER ---
def get_local_models():
    """Mengambil daftar model dari Ollama lokal."""
    try:
        response = ollama.list()
        return [m.model for m in response.models]
    except Exception:
        return []

# --- SIDEBAR: KONFIGURASI MODEL ---
st.sidebar.title("⚙️ AI Engine Config")
source_choice = st.sidebar.radio("Pilih Sumber Model:", ["Local (Ollama)", "Cloud (OpenAI/Groq)"])

llm = None
if source_choice == "Local (Ollama)":
    local_models = get_local_models()
    if local_models:
        selected_model = st.sidebar.selectbox("Pilih Model Lokal:", local_models)
        llm = OllamaLLM(model=selected_model, temperature=0)
    else:
        st.sidebar.error("Ollama tidak terdeteksi. Pastikan Ollama sudah berjalan.")
else:
    model_name = st.sidebar.text_input("Nama Model Cloud:", placeholder="gpt-4o / llama-3...")
    api_key = st.sidebar.text_input("API Key:", type="password", value=os.getenv("CLOUD_API_KEY") or "")
    base_url = st.sidebar.text_input("Base URL (Opsional):", value=os.getenv("CLOUD_BASE_URL") or "")
    
    if model_name and api_key:
        llm = ChatOpenAI(model=model_name, api_key=api_key, base_url=base_url if base_url else None, temperature=0)

# --- MAIN UI: UPLOAD DATASET ---
st.title("📊 Senior Data Scientist Agent")
st.markdown("Unggah dataset Anda (CSV/Excel) dan lakukan analisis data menggunakan AI.")

uploaded_file = st.file_uploader("Upload Dataset", type=["csv", "xlsx", "xls", "parquet", "json"])

if uploaded_file is not None:
    if "df" not in st.session_state or st.session_state.get('file_name') != uploaded_file.name:
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        try:
            # --- PENANGANAN ENCODING UNTUK CSV ---
            if ext == '.csv':
                try:
                    df_raw = pd.read_csv(uploaded_file, encoding='utf-8')
                except UnicodeDecodeError:
                    uploaded_file.seek(0)
                    df_raw = pd.read_csv(uploaded_file, encoding='latin1')
            elif ext in ['.xlsx', '.xls']:
                df_raw = pd.read_excel(uploaded_file)
            else:
                df_raw = pd.read_parquet(uploaded_file) if ext == '.parquet' else pd.read_json(uploaded_file)

            # --- NORMALISASI NAMA KOLOM ---
            # Mengubah "Temperature(°C)" menjadi "temperature_c" agar AI tidak bingung simbol
            df_raw.columns = [
                col.split('(')[0].strip().replace(' ', '_').lower() 
                for col in df_raw.columns
            ]
            
            st.session_state.df = df_raw
            st.session_state.file_name = uploaded_file.name
            st.success(f"Berhasil memuat: {uploaded_file.name} ({st.session_state.df.shape[0]} baris)")
        except Exception as e:
            st.error(f"Error membaca file: {e}")

# --- AREA CHAT DAN ANALISIS ---
if "df" in st.session_state:
    with st.expander("👀 Lihat Preview Data (Nama kolom sudah dinormalisasi)"):
        st.dataframe(st.session_state.df.head(10))

    if llm:
        # PROMPT YANG LEBIH STABIL UNTUK MENCEGAH PARSING ERROR
        CUSTOM_PROMPT = """
        Anda adalah Senior Data Analyst profesional. Anda bekerja dengan pandas DataFrame bernama `df`.
        
        WAJIB IKUTI FORMAT INI:
        Thought: [Proses berpikir Anda dalam Bahasa Indonesia]
        Action: python_repl_ast
        Action Input: [Hanya kode Python yang valid]
        Observation: [Hasil eksekusi kode]
        ... (ulangi jika perlu)
        Thought: Saya sudah menemukan jawabannya.
        Final Answer: [Jawaban akhir lengkap dalam Bahasa Indonesia beserta Insight Bisnis]

        CATATAN:
        - Jika membuat grafik, gunakan `plt.savefig('temp_plot.png')`.
        - Nama-nama kolom sudah diubah menjadi huruf kecil dan tanpa simbol (contoh: 'temperature', 'rented_bike_count').
        """

        # Inisialisasi Agent dengan penanganan error yang benar
        agent = create_pandas_dataframe_agent(
            llm, 
            st.session_state.df, 
            verbose=True, 
            allow_dangerous_code=True,
            agent_type="zero-shot-react-description", 
            prefix=CUSTOM_PROMPT,
            handle_parsing_errors=True,
        )

        # Chat History
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Input Chat
        if prompt := st.chat_input("Contoh: Tampilkan tren peminjaman sepeda per jam"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Menganalisis data..."):
                    try:
                        # Menjalankan Agent
                        response = agent.invoke({"input": prompt})
                        answer = response["output"]
                        
                        st.markdown(answer)
                        
                        # Cek jika ada gambar yang dibuat
                        if os.path.exists('temp_plot.png'):
                            st.image('temp_plot.png')
                            os.remove('temp_plot.png') # Hapus setelah ditampilkan
                            
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                    except Exception as e:
                        st.error(f"Terjadi kesalahan: {e}")
    else:
        st.info("Silakan pilih atau konfigurasi model AI di sidebar.")
else:
    st.info("Silakan unggah file dataset untuk memulai.")