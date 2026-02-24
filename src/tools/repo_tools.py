# Guidelines for repo_tools.py

# 1. Use tempfile.TemporaryDirectory for all git operations to ensure sandboxing.
# 2. Implement git log extraction to analyze commit history for atomic progression.
# 3. Use Python's ast module to verify graph structure (e.g., StateGraph instantiation).
# 4. Avoid regex for structural verification; rely on AST parsing for robustness.
# 5. Ensure all tools handle missing or invalid repositories gracefully.

import tempfile
import subprocess
import ast
from typing import List

def clone_repository(repo_url: str) -> str:
    """Clone a repository into a temporary directory."""
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            subprocess.run(["git", "clone", repo_url, temp_dir], check=True)
            return temp_dir
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to clone repository: {e}")

def analyze_graph_structure(file_path: str) -> List[str]:
    """Analyze the AST of a Python file to verify graph structure."""
    with open(file_path, "r") as file:
        tree = ast.parse(file.read())
        return [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]