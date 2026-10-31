import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from bs4 import BeautifulSoup
import requests

load_dotenv()

def scrape_website_direct(url: str) -> str:
    """Primary Route: Direct web scraping using BeautifulSoup/Requests."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            text_content = ' '.join([p.get_text() for p in paragraphs])
            return text_content[:3000] if text_content else "No paragraph content found."
        else:
            return f"Scraping blocked with status code: {response.status_code}"
    except Exception as e:
        return f"Direct Scraper Error: {str(e)}"

def fallback_web_search(query: str) -> str:
    """Fallback Route: Search via Tavily API if direct scraping fails or is blocked."""
    try:
        tavily_tool = TavilySearchResults(k=3)
        results = tavily_tool.invoke({"query": query})
        
        formatted_results = ""
        for res in results:
            formatted_results += f"\nTitle: {res.get('title', '')}\nURL: {res.get('url', '')}\nContent: {res.get('content', '')}\n---"
        return formatted_results
    except Exception as e:
        return f"Tavily Search Error: {str(e)}"

def get_market_data(query_or_url: str) -> str:
    """Smart router for data collection used by Agents."""
    if query_or_url.startswith("http://") or query_or_url.startswith("https://"):
        scraped_data = scrape_website_direct(query_or_url)
        if "Error" not in scraped_data and "blocked" not in scraped_data:
            return f"[Direct Scrape Data]:\n{scraped_data}"
    
    search_data = fallback_web_search(query_or_url)
    return f"[Tavily Search Data]:\n{search_data}"