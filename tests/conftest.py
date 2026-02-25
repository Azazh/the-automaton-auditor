import pytest
from unittest.mock import patch

@pytest.fixture
def mock_repo_path(tmp_path):
    return tmp_path / "dummy_repo"

@pytest.fixture
def mock_agent_state():
    return {
        "evidences": {},
        "logs": [],
        "opinions": []
    }
