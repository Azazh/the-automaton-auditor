# Guidelines for doc_tools.py

# 1. Use the Docling Python package for PDF parsing and chunking.
# 2. Implement a query interface to extract specific sections (e.g., "Dialectical Synthesis").
# 3. Ensure the tool handles large PDF files efficiently by chunking the content.
# 4. Cross-reference claims in the PDF with evidence collected by RepoInvestigator.
# 5. Handle missing or malformed PDF files gracefully, returning structured error messages.

from docling import PDFParser
from typing import List, Dict

def parse_pdf(file_path: str) -> Dict[str, str]:
    """
    Parse a PDF file and extract its content.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        Dict[str, str]: A dictionary where keys are section titles and values are the content.

    Raises:
        RuntimeError: If the PDF parsing fails.
    """
    try:
        parser = PDFParser(file_path)
        return parser.extract_sections()
    except Exception as e:
        raise RuntimeError(f"Failed to parse PDF: {str(e)}")

def query_pdf_content(sections: Dict[str, str], query: str) -> List[str]:
    """
    Query specific sections of a PDF for relevant content.

    Args:
        sections (Dict[str, str]): The parsed sections of the PDF.
        query (str): The query string to search for.

    Returns:
        List[str]: A list of matching content snippets.
    """
    results = []
    for title, content in sections.items():
        if query.lower() in content.lower():
            results.append(f"{title}: {content}")
    return results