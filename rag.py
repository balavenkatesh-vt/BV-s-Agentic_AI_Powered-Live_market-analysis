import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# Initialize Embedding Model (Free HuggingFace Embeddings)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def build_vector_store(text_content: str):
    """Processes scraped text, splits into chunks, and stores in ChromaDB."""
    if not text_content or "Error" in text_content:
        return None
        
    # 1. Text Chunking (500-1000 tokens/characters chunk size)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=100
    )
    docs = [Document(page_content=chunk) for chunk in text_splitter.split_text(text_content)]
    
    # 2. Store Chunks in Ephemeral/Local Chroma Vector Database
    vector_db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings
    )
    return vector_db

def query_vector_store(vector_db, query: str, k: int = 5) -> str:
    """Performs similarity search (k=5) in ChromaDB."""
    if not vector_db:
        return "No vector store available."
        
    results = vector_db.similarity_search(query, k=k)
    retrieved_text = "\n\n".join([doc.page_content for doc in results])
    return retrieved_text