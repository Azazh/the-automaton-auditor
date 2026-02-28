import tempfile
import subprocess
import os
import ast
from typing import List, Dict, Any

def clone_repo(repo_url: str, branch: str = "main") -> str:
    """
    Clone a git repository into a sandboxed temporary directory.
    Returns the path to the cloned repo.
    """
    print(f"[repo_tools] Cloning repo: {repo_url} (branch: {branch})")
    temp_dir = tempfile.mkdtemp()
    try:
        subprocess.run([
            "git", "clone", "--branch", branch, "--single-branch", repo_url, temp_dir
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"[repo_tools] Repo cloned to: {temp_dir}")
    except subprocess.CalledProcessError as e:
        print(f"[repo_tools][ERROR] Git clone failed: {e.stderr.decode()}")
        raise RuntimeError(f"Git clone failed: {e.stderr.decode()}")
    return temp_dir

def extract_git_history(repo_path: str) -> List[Dict[str, Any]]:
    """
    Extract git commit messages and timestamps from the repo.
    """
    print(f"[repo_tools] Extracting git history from: {repo_path}")
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "--reverse", "--pretty=format:%h|%ct|%s"],
            cwd=repo_path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        lines = result.stdout.decode().splitlines()
        commits = []
        for line in lines:
            parts = line.split("|", 2)
            if len(parts) == 3:
                commits.append({
                    "hash": parts[0],
                    "timestamp": int(parts[1]),
                    "message": parts[2],
                })
        print(f"[repo_tools] Found {len(commits)} commits.")
        return commits
    except subprocess.CalledProcessError as e:
        print(f"[repo_tools][ERROR] Git log failed: {e.stderr.decode()}")
        raise RuntimeError(f"Git log failed: {e.stderr.decode()}")

def find_pydantic_and_typed_dicts(pyfile: str) -> List[str]:
    """
    Find classes inheriting from BaseModel or TypedDict in a Python file.
    Returns code snippets of their definitions.
    """
    print(f"[repo_tools] Scanning for Pydantic/TypedDicts in: {pyfile}")
    if not os.path.exists(pyfile):
        print(f"[repo_tools][ERROR] File not found: {pyfile}")
        return []
    with open(pyfile, "r") as f:
        source = f.read()
    tree = ast.parse(source, filename=pyfile)
    snippets = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            bases = [b.id if isinstance(b, ast.Name) else getattr(b, 'attr', None) for b in node.bases]
            if "BaseModel" in bases or "TypedDict" in bases:
                snippet = ast.get_source_segment(source, node)
                snippets.append(snippet)
    print(f"[repo_tools] Found {len(snippets)} Pydantic/TypedDict classes.")
    return snippets

def analyze_graph_structure(repo_path: str) -> Dict[str, Any]:
    """
    Analyze the repo for StateGraph instantiation and structure using AST.
    """
    print(f"[repo_tools] Analyzing graph structure in: {repo_path}")
    graph_py = os.path.join(repo_path, "src", "graph.py")
    if not os.path.exists(graph_py):
        print("[repo_tools][ERROR] src/graph.py not found.")
        return {}
    with open(graph_py, "r") as f:
        source = f.read()
    tree = ast.parse(source, filename=graph_py)
    nodes, edges, parallel_fan_out, fan_in = [], [], False, False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and hasattr(node.func, "attr"):
            if node.func.attr == "add_edge":
                edges.append(ast.get_source_segment(source, node))
            if node.func.attr == "add_conditional_edges":
                edges.append(ast.get_source_segment(source, node))
            if node.func.attr == "add_node":
                nodes.append(ast.get_source_segment(source, node))
    parallel_fan_out = any("Detective" in str(e) for e in edges)
    fan_in = any("Aggregator" in str(e) for e in nodes)
    print(f"[repo_tools] Nodes: {len(nodes)}, Edges: {len(edges)}, Parallel: {parallel_fan_out}, Fan-in: {fan_in}")
    return {
        "nodes": nodes,
        "edges": edges,
        "parallel_fan_out": parallel_fan_out,
        "fan_in": fan_in
    }
