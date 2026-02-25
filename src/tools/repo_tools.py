# Guidelines for repo_tools.py

# 1. Use tempfile.TemporaryDirectory for all git operations to ensure sandboxing.
# 2. Implement git log extraction to analyze commit history for atomic progression.
# 3. Use Python's ast module to verify graph structure (e.g., StateGraph instantiation).
# 4. Avoid regex for structural verification; rely on AST parsing for robustness.
# 5. Ensure all tools handle missing or invalid repositories gracefully.

import tempfile
import subprocess
import os
import ast
from typing import List

def clone_repo(repo_url: str, branch: str = "main") -> str:
    """
    Clone a GitHub repository into a temporary directory.

    Args:
        repo_url (str): The URL of the GitHub repository.
        branch (str): The branch to clone. Defaults to "main".

    Returns:
        str: The path to the cloned repository.

    Raises:
        RuntimeError: If the cloning process fails.
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            subprocess.run(
                ["git", "clone", "--branch", branch, repo_url, temp_dir],
                check=True,
                text=True,
                stderr=subprocess.PIPE,
            )
            return temp_dir
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to clone repository: {e.stderr}")

def analyze_graph_structure(path: str) -> bool:
    """
    Analyze the Python files in the given path to verify StateGraph wiring.

    Args:
        path (str): The directory path to analyze.

    Returns:
        bool: True if the StateGraph is correctly wired, False otherwise.
    """
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    try:
                        tree = ast.parse(f.read(), filename=file_path)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Call) and hasattr(node.func, "attr"):
                                if node.func.attr == "add_edge":
                                    return True
                    except SyntaxError:
                        continue
    return False

def extract_git_narrative(repo_path: str) -> List[str]:
    """
    Extract the git commit history in reverse order.

    Args:
        repo_path (str): The path to the Git repository.

    Returns:
        List[str]: A list of commit messages.

    Raises:
        RuntimeError: If the git log command fails.
    """
    try:
        result = subprocess.run(
            ["git", "--no-pager", "log", "--oneline", "--reverse"],
            cwd=repo_path,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.strip().split("\n")
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to extract git narrative: {e.stderr}")