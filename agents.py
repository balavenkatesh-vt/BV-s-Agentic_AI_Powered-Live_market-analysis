import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tools import get_market_data
from rag import build_vector_store, query_vector_store

load_dotenv()

groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    raise ValueError("GROQ_API_KEY is missing! Please set it in your .env file.")

# Active & High-Rate-Limit Groq Model
llm = ChatGroq(
    api_key=groq_key,
    model_name="openai/gpt-oss-20b",  # Fast model with higher token limits
    temperature=0.3
)

def researcher_agent(prompt: str) -> str:
    """Researcher Agent: Fetches web data and builds vector store."""
    raw_data = get_market_data(prompt)
    vector_db = build_vector_store(raw_data)
    
    if vector_db:
        retrieved_context = query_vector_store(vector_db, prompt, k=5)
        return retrieved_context
    return raw_data

def analyst_agent(research_data: str, query: str) -> str:
    """Analyst Agent: Analyzes metrics, strategies, and key comparisons."""
    analysis_prompt = f"""
    You are an Expert Market Business Analyst. Analyze the following retrieved data for the query: '{query}'
    
    Data:
    {research_data}
    
    Provide structured insights covering:
    1. Key Strategies & Offerings
    2. Strengths and Weaknesses
    3. Market Metrics / Comparative Analysis
    """
    response = llm.invoke(analysis_prompt)
    return response.content

def writer_agent(analysis_data: str, query: str) -> str:
    """Writer Agent: Generates the final executive Markdown report."""
    writer_prompt = f"""
    You are a Senior Technical Content Writer.
    Transform the following analysis into a clear, professional, executive-ready Markdown report.
    
    User Query: {query}
    Analysis Data:
    {analysis_data}
    
    Structure:
    # Market Analysis Report
    ## Executive Summary
    ## Detailed Comparison
    ## Final Verdict & Recommendation
    """
    response = llm.invoke(writer_prompt)
    return response.content

def run_multi_agent_workflow(query: str):
    """Orchestrates the 3 agents in sequence."""
    print("1. Researcher Agent running...")
    research_results = researcher_agent(query)
    
    print("2. Analyst Agent processing...")
    analysis_results = analyst_agent(research_results, query)
    
    print("3. Writer Agent generating final report...")
    final_report = writer_agent(analysis_results, query)
    
    return final_report