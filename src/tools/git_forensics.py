# Git Forensics Tool: Robust, granular error handling
import os
import subprocess
from typing import List
from src.state import Evidence
from datetime import datetime
import hashlib

def get_git_commit_history(repo_path: str) -> List[Evidence]:
	"""
	Extract commit history with granular error handling.
	"""
	now = datetime.utcnow().isoformat()
	try:
		if not os.path.exists(os.path.join(repo_path, ".git")):
			raise FileNotFoundError("No .git directory found (not a git repo)")
		result = subprocess.run([
			"git", "--no-pager", "log", "--oneline", "--reverse"
		], cwd=repo_path, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		commits = result.stdout.strip().split("\n")
		if not commits or (len(commits) == 1 and not commits[0].strip()):
			raise ValueError("Empty commit history")
		evidences = []
		for idx, commit in enumerate(commits):
			sig = hashlib.sha256((repo_path + commit).encode()).hexdigest()
			evidences.append(Evidence(
				rationale=f"Commit {idx+1}: {commit}",
				source_file=repo_path,
				raw_snippet=commit,
				confidence_score=1.0,
				verification_method="Git-Log",
				raw_output=commit,
				analysis_timestamp=now,
				forensic_signature=sig
			))
		return evidences
	except FileNotFoundError as e:
		sig = hashlib.sha256((repo_path + str(e)).encode()).hexdigest()
		return [Evidence(
			rationale=f"Git repo not found: {e}",
			source_file=repo_path,
			raw_snippet="",
			confidence_score=0.0,
			verification_method="Git-Log-Error",
			raw_output=str(e),
			analysis_timestamp=now,
			forensic_signature=sig
		)]
	except subprocess.CalledProcessError as e:
		msg = e.stderr.strip()
		if "not a git repository" in msg:
			rationale = "Not a git repository (detached HEAD or missing .git)"
		elif "permission denied" in msg.lower():
			rationale = "Permission error accessing git repo"
		else:
			rationale = f"Git error: {msg}"
		sig = hashlib.sha256((repo_path + rationale).encode()).hexdigest()
		return [Evidence(
			rationale=rationale,
			source_file=repo_path,
			raw_snippet="",
			confidence_score=0.0,
			verification_method="Git-Log-Error",
			raw_output=msg,
			analysis_timestamp=now,
			forensic_signature=sig
		)]
	except ValueError as e:
		sig = hashlib.sha256((repo_path + str(e)).encode()).hexdigest()
		return [Evidence(
			rationale=f"Empty commit history: {e}",
			source_file=repo_path,
			raw_snippet="",
			confidence_score=0.0,
			verification_method="Git-Log-Error",
			raw_output=str(e),
			analysis_timestamp=now,
			forensic_signature=sig
		)]
	except Exception as e:
		sig = hashlib.sha256((repo_path + str(e)).encode()).hexdigest()
		return [Evidence(
			rationale=f"Unknown git error: {type(e).__name__}: {e}",
			source_file=repo_path,
			raw_snippet="",
			confidence_score=0.0,
			verification_method="Git-Log-Error",
			raw_output=str(e),
			analysis_timestamp=now,
			forensic_signature=sig
		)]
