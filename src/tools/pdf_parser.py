# PDF Parser with Chunking and RAG-like Retrieval
import os
from typing import List, Dict, Optional
from PyPDF2 import PdfReader
from src.state import Evidence
from datetime import datetime
import hashlib

def chunk_pdf_text(text: str, chunk_size: int = 500) -> List[str]:
	"""
	Split text into semantic chunks of approximately chunk_size characters.
	"""
	paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
	chunks = []
	current = ""
	for para in paragraphs:
		if len(current) + len(para) < chunk_size:
			current += ("\n" if current else "") + para
		else:
			if current:
				chunks.append(current)
			current = para
	if current:
		chunks.append(current)
	return chunks

def parse_pdf(path: str) -> List[str]:
	"""
	Extract all text from a PDF file and return as a list of pages.
	"""
	reader = PdfReader(path)
	return [page.extract_text() or "" for page in reader.pages]

def pdf_to_chunks(pdf_path: str, chunk_size: int = 500) -> List[Dict]:
	"""
	Parse PDF and return a list of chunk dicts with page and chunk index.
	"""
	pages = parse_pdf(pdf_path)
	all_chunks = []
	for page_num, page_text in enumerate(pages):
		chunks = chunk_pdf_text(page_text, chunk_size)
		for chunk_idx, chunk in enumerate(chunks):
			all_chunks.append({
				"page": page_num + 1,
				"chunk_index": chunk_idx,
				"text": chunk
			})
	return all_chunks

def query_pdf_chunks(pdf_path: str, query: Optional[str] = None, chunk_size: int = 500) -> List[Evidence]:
	"""
	Query PDF chunks for a keyword or phrase. If no query, return all chunks as evidence.
	"""
	chunks = pdf_to_chunks(pdf_path, chunk_size)
	results = []
	for chunk in chunks:
		if query is None or query.lower() in chunk["text"].lower():
			now = datetime.utcnow().isoformat()
			sig = hashlib.sha256((pdf_path + str(chunk["page"]) + str(chunk["chunk_index"]) + chunk["text"]).encode()).hexdigest()
			results.append(Evidence(
				rationale=f"PDF chunk from page {chunk['page']} (chunk {chunk['chunk_index']}) matching query '{query}'" if query else f"PDF chunk from page {chunk['page']} (chunk {chunk['chunk_index']})",
				source_file=pdf_path,
				raw_snippet=chunk["text"][:200],
				confidence_score=1.0,
				verification_method="PDF-Chunk-RAG",
				raw_output=chunk["text"][:200],
				analysis_timestamp=now,
				forensic_signature=sig
			))
	return results
