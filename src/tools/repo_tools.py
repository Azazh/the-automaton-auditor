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
from typing import List, Dict, Any
from src.state import Evidence
from datetime import datetime
import hashlib

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

def ast_structural_evidence(path: str) -> Evidence:
    """
    Forensic AST scan for interim checklist:
      - Does src/state.py use BaseModel?
      - Does src/graph.py use StateGraph?
    Returns rich Evidence for each finding.
    """
    findings = []
    checklist = [
        ("src/state.py", "BaseModel"),
        ("src/graph.py", "StateGraph"),
    ]
    # Additional checks for inheritance and function calls
    inheritance_checks = [
        ("src/state.py", "BaseModel"),
    ]
    function_call_checks = [
        ("src/state.py", ["operator.add", "operator.ior"]),
    ]
    for file_path, symbol in checklist:
        abs_path = os.path.join(path, file_path)
        try:
            with open(abs_path, "r") as f:
                code = f.read()
                tree = ast.parse(code, filename=abs_path)
                found = any(
                    (isinstance(node, ast.Name) and node.id == symbol) or
                    (isinstance(node, ast.Attribute) and node.attr == symbol)
                    for node in ast.walk(tree)
                )
                snippet = code if found else ""
                now = datetime.utcnow().isoformat()
                sig = hashlib.sha256((file_path + symbol + snippet).encode()).hexdigest()
                findings.append(Evidence(
                    rationale=f"Checked for {symbol} in {file_path}.",
                    source_file=file_path,
                    raw_snippet=snippet[:200],
                    confidence_score=1.0 if found else 0.0,
                    verification_method="AST-Analysis",
                    raw_output=snippet[:200],
                    analysis_timestamp=now,
                    forensic_signature=sig
                ))
        except Exception as e:
            now = datetime.utcnow().isoformat()
            sig = hashlib.sha256((file_path + str(e)).encode()).hexdigest()
            findings.append(Evidence(
                rationale=f"Error parsing {file_path}: {type(e).__name__}: {e}",
                source_file=file_path,
                raw_snippet="",
                confidence_score=0.0,
                verification_method="AST-Analysis",
                raw_output=str(e),
                analysis_timestamp=now,
                forensic_signature=sig
            ))
    # Inheritance checks
    for file_path, base_class in inheritance_checks:
        abs_path = os.path.join(path, file_path)
        try:
            with open(abs_path, "r") as f:
                code = f.read()
                tree = ast.parse(code, filename=abs_path)
                found = False
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        for base in node.bases:
                            if (isinstance(base, ast.Name) and base.id == base_class) or \
                               (isinstance(base, ast.Attribute) and base.attr == base_class):
                                found = True
                                snippet = code[node.lineno-1:node.end_lineno] if hasattr(node, 'end_lineno') else code
                                now = datetime.utcnow().isoformat()
                                sig = hashlib.sha256((file_path + base_class + str(node.lineno)).encode()).hexdigest()
                                findings.append(Evidence(
                                    rationale=f"Class inherits from {base_class} in {file_path} at line {node.lineno}.",
                                    source_file=file_path,
                                    raw_snippet=snippet[:200],
                                    confidence_score=1.0,
                                    verification_method="AST-Inheritance-Check",
                                    raw_output=snippet[:200],
                                    analysis_timestamp=now,
                                    forensic_signature=sig
                                ))
                if not found:
                    now = datetime.utcnow().isoformat()
                    sig = hashlib.sha256((file_path + base_class + "notfound").encode()).hexdigest()
                    findings.append(Evidence(
                        rationale=f"No class inherits from {base_class} in {file_path}.",
                        source_file=file_path,
                        raw_snippet="",
                        confidence_score=0.0,
                        verification_method="AST-Inheritance-Check",
                        raw_output="",
                        analysis_timestamp=now,
                        forensic_signature=sig
                    ))
        except Exception as e:
            now = datetime.utcnow().isoformat()
            sig = hashlib.sha256((file_path + str(e)).encode()).hexdigest()
            findings.append(Evidence(
                rationale=f"Error parsing {file_path} for inheritance: {type(e).__name__}: {e}",
                source_file=file_path,
                raw_snippet="",
                confidence_score=0.0,
                verification_method="AST-Inheritance-Check",
                raw_output=str(e),
                analysis_timestamp=now,
                forensic_signature=sig
            ))
    # Function call checks
    for file_path, call_list in function_call_checks:
        abs_path = os.path.join(path, file_path)
        try:
            with open(abs_path, "r") as f:
                code = f.read()
                tree = ast.parse(code, filename=abs_path)
                for call in call_list:
                    found = False
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Call):
                            func = node.func
                            if isinstance(func, ast.Attribute):
                                full_name = f"{getattr(func.value, 'id', '')}.{func.attr}"
                                if full_name == call:
                                    found = True
                                    snippet = code[node.lineno-1:node.end_lineno] if hasattr(node, 'end_lineno') else code
                                    now = datetime.utcnow().isoformat()
                                    sig = hashlib.sha256((file_path + call + str(node.lineno)).encode()).hexdigest()
                                    findings.append(Evidence(
                                        rationale=f"Function call {call} found in {file_path} at line {node.lineno}.",
                                        source_file=file_path,
                                        raw_snippet=snippet[:200],
                                        confidence_score=1.0,
                                        verification_method="AST-Call-Check",
                                        raw_output=snippet[:200],
                                        analysis_timestamp=now,
                                        forensic_signature=sig
                                    ))
                    if not found:
                        now = datetime.utcnow().isoformat()
                        sig = hashlib.sha256((file_path + call + "notfound").encode()).hexdigest()
                        findings.append(Evidence(
                            rationale=f"Function call {call} not found in {file_path}.",
                            source_file=file_path,
                            raw_snippet="",
                            confidence_score=0.0,
                            verification_method="AST-Call-Check",
                            raw_output="",
                            analysis_timestamp=now,
                            forensic_signature=sig
                        ))
        except Exception as e:
            now = datetime.utcnow().isoformat()
            sig = hashlib.sha256((file_path + str(e)).encode()).hexdigest()
            findings.append(Evidence(
                rationale=f"Error parsing {file_path} for calls: {type(e).__name__}: {e}",
                source_file=file_path,
                raw_snippet="",
                confidence_score=0.0,
                verification_method="AST-Call-Check",
                raw_output=str(e),
                analysis_timestamp=now,
                forensic_signature=sig
            ))
    return findings

def analyze_graph_structure(path: str) -> Dict[str, List[str]]:
    """
    Analyze the Python files in the given path to verify StateGraph wiring.

    Args:
        path (str): The directory path to analyze.

    Returns:
        Dict[str, List[str]]: A mapping of node names to their connected edges.
    """
    graph_structure = {}

    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    try:
                        tree = ast.parse(f.read(), filename=file_path)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                                if node.func.attr in {"add_fan_out", "add_fan_in", "add_edge"}:
                                    args = [arg.s for arg in node.args if isinstance(arg, ast.Constant)]
                                    graph_structure[node.func.attr] = graph_structure.get(node.func.attr, []) + args
                    except Exception as e:
                        print(f"Error parsing {file_path}: {e}")

    return graph_structure

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