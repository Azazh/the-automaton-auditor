# Guidelines for doc_tools.py

# 1. Use the Docling Python package for PDF parsing and chunking.
# 2. Implement a query interface to extract specific sections (e.g., "Dialectical Synthesis").
# 3. Ensure the tool handles large PDF files efficiently by chunking the content.
# 4. Cross-reference claims in the PDF with evidence collected by RepoInvestigator.
# 5. Handle missing or malformed PDF files gracefully, returning structured error messages.