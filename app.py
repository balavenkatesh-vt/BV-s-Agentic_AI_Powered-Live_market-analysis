import streamlit as st
import io
import re
import html
import unicodedata
import speech_recognition as sr
from agents import run_multi_agent_workflow
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Streamlit Page Config
st.set_page_config(
    page_title="Agentic AI - Live Market Analysis",
    page_icon="📊",
    layout="wide"
)

# PDF Utility Functions
def clean_unicode_text(text: str) -> str:
    replacements = {
        '–': '-', '—': '-', '’': "'", '‘': "'", '“': '"', '”': '"',
        '•': '*', '…': '...', '₹': 'Rs. ', '™': '(TM)', '®': '(R)', '©': '(C)',
    }
    for orig, repl in replacements.items():
        text = text.replace(orig, repl)
    normalized = unicodedata.normalize('NFKD', text)
    return normalized.encode('ascii', 'ignore').decode('ascii')

def generate_pdf(text_content):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    custom_style = ParagraphStyle('Normal', parent=styles['Normal'], fontSize=9, leading=12)
    header_style = ParagraphStyle('HeaderStyle', parent=styles['Normal'], fontSize=9, leading=12, textColor=colors.white, fontName='Helvetica-Bold')
    
    cleaned_content = clean_unicode_text(text_content)
    story = []
    lines = cleaned_content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('|') and '|' in line[1:]:
            table_data = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                row_line = lines[i].strip()
                if not re.match(r'^\|[\s:\|-]+\|$', row_line):
                    cells = [c.strip() for c in row_line.split('|')[1:-1]]
                    row_cells = []
                    for c in cells:
                        clean_c = html.escape(c)
                        clean_c = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', clean_c)
                        p_style = header_style if len(table_data) == 0 else custom_style
                        row_cells.append(Paragraph(clean_c, p_style))
                    table_data.append(row_cells)
                i += 1
            if table_data:
                t = Table(table_data, colWidths=None)
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('VALIGN', (0,0), (-1,-1), 'TOP'),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                    ('TOPPADDING', (0,0), (-1,-1), 6),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
                    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
                ]))
                story.append(t)
                story.append(Spacer(1, 10))
            continue
        elif line:
            clean_line = html.escape(line)
            clean_line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', clean_line)
            clean_line = re.sub(r'^#+\s*', '', clean_line)
            story.append(Paragraph(clean_line, custom_style))
            story.append(Spacer(1, 4))
        i += 1
            
    doc.build(story)
    buffer.seek(0)
    return buffer

# Main UI Header
st.title("📊 BV's Agentic AI Powered Live Market Competition Analysis")
st.markdown("Multi-Agent System powered by **LangGraph**, **ChromaDB**, and **Groq LLM**")

# Initialize Session States
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "main_query_text_box" not in st.session_state:
    st.session_state.main_query_text_box = ""

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Controls & Options")
    if st.button("🗑️ Clear Chat History", type="secondary", key="clear_chat_history_btn"):
        st.session_state.chat_history = []
        st.session_state.main_query_text_box = ""
        st.rerun()

st.divider()

# Callback Function: Transcribes Recorded Audio directly to Text Box Key
def on_audio_change():
    audio_file = st.session_state.audio_recorder_input
    if audio_file is not None:
        r = sr.Recognizer()
        try:
            with sr.AudioFile(audio_file) as source:
                audio_data = r.record(source)
                transcribed = r.recognize_google(audio_data, language="en-US")
                if transcribed:
                    # Update text input key directly inside callback
                    st.session_state.main_query_text_box = transcribed
        except Exception:
            pass

# Audio Recording Input with Callback
st.write("🎙️ **Voice Search (Record & Auto-Fill)**")
st.audio_input(
    "Click mic icon to record voice query",
    key="audio_recorder_input",
    on_change=on_audio_change
)

# Text Search Box (Bound directly to session state key)
user_query = st.text_input(
    "Enter Market Analysis Query / Competitors to Compare:",
    placeholder="e.g., Compare Lay's vs Bingo vs Kurkure",
    key="main_query_text_box"
)

# Analysis Execution Button
if st.button("🚀 Run BV's Agentic Analysis", type="primary", key="run_analysis_submit_btn"):
    final_query = user_query.strip()
    
    if not final_query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("🤖 BV's Multi-Agent Workflow running (Researcher ➔ Analyst ➔ Writer)..."):
            try:
                report = run_multi_agent_workflow(final_query)
                st.session_state.chat_history.append({
                    "query": final_query,
                    "report": report
                })
                st.rerun()
            except Exception as e:
                st.error(f"Error during analysis: {str(e)}")

# Historical Reports
if st.session_state.chat_history:
    st.subheader("📜 Analysis History & Reports")
    for idx, item in enumerate(reversed(st.session_state.chat_history)):
        chat_index = len(st.session_state.chat_history) - idx
        with st.expander(f"📌 Analysis #{chat_index}: {item['query']}", expanded=(idx == 0)):
            st.markdown(item["report"])
            pdf_data = generate_pdf(item["report"])
            st.download_button(
                label="📥 Download Report as PDF",
                data=pdf_data,
                file_name=f"Market_Analysis_{chat_index}.pdf",
                mime="application/pdf",
                key=f"pdf_download_btn_{chat_index}_{idx}"
            )
            st.divider()