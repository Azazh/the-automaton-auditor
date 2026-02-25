from langgraph import Node
from src.tools.repo_tools import clone_repo, analyze_graph_structure, extract_git_narrative
from src.tools.doc_tools import parse_pdf, query_pdf_content
from src.state import Evidence
from typing import Dict
from datetime import datetime
import hashlib

class RepoInvestigator(Node):
    async def run(self, repo_url: str, branch: str = "main") -> Dict[str, Evidence]:
        """
        Investigate a repository and collect evidence.

        Args:
            repo_url (str): The URL of the GitHub repository.
            branch (str): The branch to analyze. Defaults to "main".

        Returns:
            Dict[str, Evidence]: A dictionary of Evidence objects.
        """
        evidences = {}
        try:
            repo_path = clone_repo(repo_url, branch)
            graph_valid = analyze_graph_structure(repo_path)
            git_history = extract_git_narrative(repo_path)
            now = datetime.utcnow().isoformat()

            # Graph structure evidence
            raw_graph = str(graph_valid)
            graph_hash = hashlib.sha256(raw_graph.encode()).hexdigest()
            evidences["graph_structure"] = Evidence(
                rationale="Verified StateGraph wiring.",
                confidence=1.0 if graph_valid else 0.5,
                source="AST analysis",
                raw_output=raw_graph,
                analysis_timestamp=now,
                forensic_signature=graph_hash
            )

            # Git narrative evidence
            raw_git = str(git_history)
            git_hash = hashlib.sha256(raw_git.encode()).hexdigest()
            evidences["git_narrative"] = Evidence(
                rationale="Extracted git commit history.",
                confidence=1.0,
                source="Git log",
                raw_output=raw_git,
                analysis_timestamp=now,
                forensic_signature=git_hash
            )
        except Exception as e:
            now = datetime.utcnow().isoformat()
            err_raw = str(e)
            err_hash = hashlib.sha256(err_raw.encode()).hexdigest()
            evidences["error"] = Evidence(
                rationale=f"Failed to investigate repo: {str(e)}",
                confidence=0.0,
                source="RepoInvestigator",
                raw_output=err_raw,
                analysis_timestamp=now,
                forensic_signature=err_hash
            )
        return evidences

class DocAnalyst(Node):
    async def run(self, pdf_path: str, query: str) -> Dict[str, Evidence]:
        """
        Analyze a PDF document and collect evidence.

        Args:
            pdf_path (str): The path to the PDF file.
            query (str): The query string to search for in the document.

        Returns:
            Dict[str, Evidence]: A dictionary of Evidence objects.
        """
        evidences = {}
        try:
            sections = parse_pdf(pdf_path)
            results = query_pdf_content(sections, query)
            now = datetime.utcnow().isoformat()
            raw_pdf = str(results)
            pdf_hash = hashlib.sha256(raw_pdf.encode()).hexdigest()
            evidences["pdf_analysis"] = Evidence(
                rationale=f"Queried PDF for '{query}'. Found {len(results)} relevant sections.",
                confidence=1.0 if results else 0.5,
                source="PDF analysis",
                raw_output=raw_pdf,
                analysis_timestamp=now,
                forensic_signature=pdf_hash
            )
        except Exception as e:
            now = datetime.utcnow().isoformat()
            err_raw = str(e)
            err_hash = hashlib.sha256(err_raw.encode()).hexdigest()
            evidences["error"] = Evidence(
                rationale=f"Failed to analyze PDF: {str(e)}",
                confidence=0.0,
                source="DocAnalyst",
                raw_output=err_raw,
                analysis_timestamp=now,
                forensic_signature=err_hash
            )
        return evidences