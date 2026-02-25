import tempfile
from src.tools.repo_tools import ast_structural_evidence, clone_repo
from src.state import Evidence
from unittest.mock import patch

def test_ast_structural_evidence_missing_stategraph(tmp_path):
    dummy_file = tmp_path / "dummy.py"
    dummy_file.write_text("# No StateGraph here\n")
    # Should not raise, should return Evidence with confidence_score 0.0
    evidences = ast_structural_evidence(str(tmp_path))
    found = any(ev.confidence_score == 0.0 for ev in evidences)
    assert found

@patch("subprocess.run")
def test_clone_repo_invalid_url(mock_run):
    mock_run.side_effect = Exception("Invalid URL")
    try:
        clone_repo("invalid_url")
    except RuntimeError as e:
        assert "Failed to clone repository" in str(e)
