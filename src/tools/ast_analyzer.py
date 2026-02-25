# AST Analyzer: Structural, Inheritance, and Call Checks
import ast
from typing import List, Dict, Any, Optional
from src.state import Evidence
from datetime import datetime
import hashlib

def analyze_inheritance(source_code: str, base_class: str, file_path: str) -> List[Evidence]:
	"""
	Check if any class in the source code inherits from base_class.
	"""
	results = []
	try:
		tree = ast.parse(source_code, filename=file_path)
		found = False
		for node in ast.walk(tree):
			if isinstance(node, ast.ClassDef):
				for base in node.bases:
					if (isinstance(base, ast.Name) and base.id == base_class) or \
					   (isinstance(base, ast.Attribute) and base.attr == base_class):
						found = True
						snippet = ast.get_source_segment(source_code, node) or ""
						now = datetime.utcnow().isoformat()
						sig = hashlib.sha256((file_path + base_class + str(node.lineno)).encode()).hexdigest()
						results.append(Evidence(
							rationale=f"Class '{node.name}' inherits from {base_class} at line {node.lineno}.",
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
			results.append(Evidence(
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
		results.append(Evidence(
			rationale=f"Error parsing {file_path} for inheritance: {type(e).__name__}: {e}",
			source_file=file_path,
			raw_snippet="",
			confidence_score=0.0,
			verification_method="AST-Inheritance-Check",
			raw_output=str(e),
			analysis_timestamp=now,
			forensic_signature=sig
		))
	return results

def analyze_function_calls(source_code: str, call_names: List[str], file_path: str) -> List[Evidence]:
	"""
	Check if specific function calls (e.g., operator.add) are present in the source code.
	"""
	results = []
	try:
		tree = ast.parse(source_code, filename=file_path)
		for call in call_names:
			found = False
			for node in ast.walk(tree):
				if isinstance(node, ast.Call):
					func = node.func
					if isinstance(func, ast.Attribute):
						full_name = f"{getattr(func.value, 'id', '')}.{func.attr}"
						if full_name == call:
							found = True
							snippet = ast.get_source_segment(source_code, node) or ""
							now = datetime.utcnow().isoformat()
							sig = hashlib.sha256((file_path + call + str(node.lineno)).encode()).hexdigest()
							results.append(Evidence(
								rationale=f"Function call {call} found at line {node.lineno}.",
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
				results.append(Evidence(
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
		results.append(Evidence(
			rationale=f"Error parsing {file_path} for calls: {type(e).__name__}: {e}",
			source_file=file_path,
			raw_snippet="",
			confidence_score=0.0,
			verification_method="AST-Call-Check",
			raw_output=str(e),
			analysis_timestamp=now,
			forensic_signature=sig
		))
	return results

def analyze_structural_presence(source_code: str, symbols: List[str], file_path: str) -> List[Evidence]:
	"""
	Check for presence of specific symbols (e.g., BaseModel, StateGraph) in the AST.
	"""
	results = []
	try:
		tree = ast.parse(source_code, filename=file_path)
		for symbol in symbols:
			found = any(
				(isinstance(node, ast.Name) and node.id == symbol) or
				(isinstance(node, ast.Attribute) and node.attr == symbol)
				for node in ast.walk(tree)
			)
			snippet = symbol if found else ""
			now = datetime.utcnow().isoformat()
			sig = hashlib.sha256((file_path + symbol + snippet).encode()).hexdigest()
			results.append(Evidence(
				rationale=f"Checked for {symbol} in {file_path}.",
				source_file=file_path,
				raw_snippet=snippet[:200],
				confidence_score=1.0 if found else 0.0,
				verification_method="AST-Structural-Check",
				raw_output=snippet[:200],
				analysis_timestamp=now,
				forensic_signature=sig
			))
	except Exception as e:
		now = datetime.utcnow().isoformat()
		sig = hashlib.sha256((file_path + str(e)).encode()).hexdigest()
		results.append(Evidence(
			rationale=f"Error parsing {file_path} for symbols: {type(e).__name__}: {e}",
			source_file=file_path,
			raw_snippet="",
			confidence_score=0.0,
			verification_method="AST-Structural-Check",
			raw_output=str(e),
			analysis_timestamp=now,
			forensic_signature=sig
		))
	return results
