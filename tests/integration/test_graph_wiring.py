from src.graph import graph

def test_graph_start_fan_out():
    # graph.edges is a set of (start, end) tuples in langgraph 0.0.40
    start_edges = [end for (start, end) in graph.edges if start == "START"]
    assert "repo_investigator" in start_edges
    assert "doc_analyst" in start_edges
    assert len(start_edges) >= 2
