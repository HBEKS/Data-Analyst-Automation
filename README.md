# 📊 AI Data Analyst Specialist Agent

> **Note:** This project was developed as a prerequisite final project for the **dsarea.id AI Engineer Bootcamp**.

An advanced data science assistant that leverages Large Language Models (LLMs) to perform automated data analysis, visualization, and insight generation. This tool allows users to interact with their datasets using natural language.

## 🌟 Background

This project demonstrates the implementation of **Agentic AI** in the field of Data Science. By using the ReAct (Reasoning and Acting) framework, the agent can "think" about a data problem, "act" by writing and executing Python code, and "observe" the results to provide professional business insights.

## 🚀 Features

- **Hybrid AI Engine**: Switch between **Local Models** (via Ollama) for privacy and **Cloud Models** (OpenAI/Groq) for high performance.
- **Multi-format Support**: Upload datasets in CSV, Excel (XLSX/XLS), Parquet, or JSON formats.
- **Automated Data Cleaning**: Automatic column normalization (lowercase, snake_case, and symbol removal) to optimize AI reasoning.
- **Interactive Visualization**: Generates charts and graphs (Matplotlib/Seaborn) based on natural language queries.
- **Senior Analyst Logic**: Uses LangChain's `create_pandas_dataframe_agent` with a custom prompt for high-accuracy Indonesian responses.

## 🛠️ Tech Stack

- **Framework**: [Streamlit](https://streamlit.io/)
- **Orchestration**: [LangChain](https://www.langchain.com/)
- **Data Handling**: [Pandas](https://pandas.pydata.org/)
- **Local LLM**: [Ollama](https://ollama.com/)
- **Cloud LLM**: [OpenAI GPT-4o / Groq](https://openai.com/)

## 📋 Prerequisites

Before running the application, ensure you have:

1. Python 3.10 or higher
2. [Ollama](https://ollama.com/) installed and running (if using local models)
3. API Keys for OpenAI or Groq (if using cloud models)

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/HBEKS/Data-Analyst-Automation.git
cd Data-Analyst-Automation'''

### **2. Create a Virtual Environment:**
'''bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
'''

### **3. Install Dependencies:**
'''bash
pip install -r requirements.txt
'''

### **4. Environment Variables:**
Create a .env file in the root directory:
'''bash
CLOUD_API_KEY=your_api_key_here
CLOUD_BASE_URL=[https://api.openai.com/v1](https://api.openai.com/v1)
'''

### 🏃 **Running the App**
Start the Streamlit server:
'''bash
streamlit run main.py
'''

## 💡 Usage Guide

To start analyzing your data, follow these simple steps within the application interface:

1. **Configure AI Engine**: 
   - Open the **Sidebar** on the left.
   - Choose **Local (Ollama)** if you want to run models on your own hardware (privacy-focused).
   - Choose **Cloud (OpenAI/Groq)** for faster processing and advanced reasoning.

2. **Upload Dataset**: 
   - Use the file uploader in the main area.
   - Supported formats: `.csv`, `.xlsx`, `.xls`, `.parquet`, or `.json`.
   - *Note: The agent automatically cleans and normalizes column names for better AI compatibility.*

3. **Interact with Your Data**: 
   Type your questions in the chat input at the bottom. You can try commands like:
   * 📋 **Inspection**: *"Tampilkan 5 baris pertama data ini untuk melihat strukturnya."*
   * 🔍 **Analysis**: *"Apa korelasi antara suhu (temperature) dan jumlah penyewaan sepeda?"*
   * 📈 **Visualization**: *"Buatlah grafik garis yang menunjukkan tren penjualan bulanan."*
   * 🧠 **Business Insight**: *"Berdasarkan data ini, berikan 3 rekomendasi strategi untuk meningkatkan penjualan."*

---

## 👨‍💻 Author

**Daniel Wuliutomo** *Informatics Engineering Student — University of Surabaya (Ubaya)* *AI Engineer Bootcamp Participant — [dsarea.id](https://dsarea.id)*

---
