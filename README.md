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