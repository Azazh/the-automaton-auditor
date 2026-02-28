import operator
from src.state import JudicialOpinion, Evidence, AgentState

def test_operator_ior_merges_evidence_dicts():
    dict1 = {"a": Evidence(rationale="A", source_file="file1.py", raw_snippet="", confidence_score=1.0, verification_method="AST-Analysis", raw_output="", analysis_timestamp="", forensic_signature="")}
    dict2 = {"b": Evidence(rationale="B", source_file="file2.py", raw_snippet="", confidence_score=0.9, verification_method="Docling-Parsing", raw_output="", analysis_timestamp="", forensic_signature="")}
    merged = operator.ior(dict1.copy(), dict2)
    assert merged["a"].rationale == "A"
    assert merged["b"].rationale == "B"
    assert len(merged) == 2

def test_operator_add_appends_logs():
    logs1 = ["log1"]
    logs2 = ["log2"]
    merged = operator.add(logs1, logs2)
    assert merged == ["log1", "log2"]
