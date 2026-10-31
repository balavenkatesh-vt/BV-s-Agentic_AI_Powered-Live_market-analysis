# 📊 BV's Agentic AI Powered - Live Market Competition Analysis

An end-to-end Multi-Agent AI system designed to conduct real-time, on-demand market competition research, comparative analysis, and report generation using **LangGraph**, **Groq LLM**, **Tavily Web Search**, and **ChromaDB**. 

The application features a modern Streamlit user interface supporting **Voice Search**, **Editable Text Input**, and **Professional PDF Exports**.

---

## 🌟 Key Features

* **🤖 Multi-Agent Workflow (LangGraph):**
  * **Researcher Agent:** Scrapes real-time competitive intelligence from the web using Tavily API.
  * **Analyst Agent:** Synthesizes raw data, performs SWOT analysis, and extracts key benchmarks.
  * **Writer Agent:** Formats structured, professional executive summaries and tabular reports.
* **🎙️ Dual Input Options:**
  * **Voice Search:** Speech-to-Text conversion via Streamlit Audio & Google Speech Recognition with real-time UI synchronization.
  * **Manual Search:** Editable text input bar for flexible query adjustments.
* **📚 Dynamic RAG Architecture:** Vector embedding and context retrieval powered by **ChromaDB**.
* **📥 One-Click PDF Export:** Automatically generates styled PDF reports with dynamic tables using **ReportLab** (with full Unicode cleaning).
* **☁️ Cloud-Ready & Secure:** Configured with `.gitignore` and `packages.txt` for seamless deployment on **Streamlit Community Cloud**.

---

## 🏗️ System Architecture

```text
User Input (Voice / Text)
       │
       ▼
  Streamlit UI ──► ChromaDB (Vector Store / RAG)
       │
       ▼
LangGraph Multi-Agent Workflow
       │
       ├──► 1. Researcher Agent (Tavily Web Scraper)
       ├──► 2. Analyst Agent (Market Benchmark & SWOT)
       └──► 3. Writer Agent (Groq Llama-3 / GPT-OSS-20B)
       │
       ▼
Interactive Report + PDF Generator (ReportLab)

🛠️ Tech Stack
Frontend: Streamlit

Agent Framework: LangGraph, LangChain

LLM Provider: Groq API (openai/gpt-oss-20b / llama-3.3-70b-versatile)

Web Search Engine: Tavily Search API

Vector Store: ChromaDB

Audio Processing: SpeechRecognition

Document Generation: ReportLab

Version Control & Hosting: Git, GitHub, Streamlit Cloud

📁 Repository Structure
Plaintext
├── app.py              # Streamlit Web Application Interface & Session Sync
├── agents.py           # LangGraph Multi-Agent Nodes & State Definition
├── tools.py            # Tavily Search Tool & Web Scraper Utilities
├── rag.py              # ChromaDB Initialization & Vector RAG Pipeline
├── requirements.txt    # Python Dependencies
├── packages.txt        # Linux System Dependencies (for Cloud Build)
├── .gitignore          # Excluded Files (.env, venv, chroma_db, PDFs)
└── README.md           # Project Documentation
🚀 Quickstart Guide
1. Prerequisites
Ensure you have Python 3.10 or higher installed on your machine.

2. Clone Repository
Bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/agentic-market-analysis.git](https://github.com/YOUR_GITHUB_USERNAME/agentic-market-analysis.git)
cd agentic-market-analysis
3. Set Up Virtual Environment
Bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
4. Install Dependencies
Bash
pip install -r requirements.txt
5. Environment Variables Setup
Create a .env file in the root directory and add your API keys:

Code snippet
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
6. Run Application Locally
Bash
streamlit run app.py
☁️ Streamlit Cloud Deployment
Push your repository to GitHub.   
logs-balavenkatesh-vt-bv-s-agentic_ai_powered-live_market-analysis-main-app.py-2026-10-31T16_33_04.117Z.txt

Visit share.streamlit.io and log in with GitHub.   
logs-balavenkatesh-vt-bv-s-agentic_ai_powered-live_market-analysis-main-app.py-2026-10-31T16_33_04.117Z.txt

Click Create app and select your repository, branch (main), and file (app.py).   
logs-balavenkatesh-vt-bv-s-agentic_ai_powered-live_market-analysis-main-app.py-2026-10-31T16_33_04.117Z.txt

Under Advanced Settings ➔ Secrets, paste your API keys:

Ini, TOML
GROQ_API_KEY = "your_groq_api_key_here"
TAVILY_API_KEY = "your_tavily_api_key_here"
Click Deploy!

📜 License
This project is open-source and available under the MIT License.