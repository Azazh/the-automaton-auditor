from typing import List, Dict
from PyPDF2 import PdfReader
import os

def parse_pdf(pdf_path: str) -> List[str]:
    """
    Parse a PDF into a list of text sections (one per page).
    """
    print(f"[doc_tools] Parsing PDF: {pdf_path}")
    if not os.path.exists(pdf_path):
        print("[doc_tools][ERROR] PDF not found.")
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    reader = PdfReader(pdf_path)
    sections = [page.extract_text() or "" for page in reader.pages]
    print(f"[doc_tools] Extracted {len(sections)} pages.")
    return sections

def chunk_sections(sections: List[str], chunk_size: int = 500) -> List[str]:
    """
    Chunk PDF sections into smaller pieces for RAG-lite querying.
    """
    print(f"[doc_tools] Chunking sections with chunk size: {chunk_size}")
    chunks = []
    for section in sections:
        for i in range(0, len(section), chunk_size):
            chunks.append(section[i:i+chunk_size])
    print(f"[doc_tools] Created {len(chunks)} chunks.")
    return chunks

def query_pdf_content(sections: List[str], query: str) -> List[str]:
    """
    Simple keyword search for relevant sections in the PDF.
    """
    print(f"[doc_tools] Querying PDF for: {query}")
    results = []
    for section in sections:
        if query.lower() in section.lower():
            results.append(section)
    print(f"[doc_tools] Found {len(results)} relevant sections.")
    return results

def ingest_pdf(pdf_path: str, query: str) -> List[str]:
    """
    Ingest and query a PDF for specific content (RAG-lite).
    """
    print(f"[doc_tools] Ingesting PDF for query: {query}")
    sections = parse_pdf(pdf_path)
    chunks = chunk_sections(sections)
    return query_pdf_content(chunks, query)
