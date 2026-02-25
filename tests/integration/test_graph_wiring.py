from src.graph import graph

def test_graph_start_fan_out():
    nodes = graph.nodes
    start_edges = graph.edges.get("START", [])
    node_names = [n.__class__.__name__ for n in start_edges]
    assert "RepoInvestigator" in node_names
    assert "DocAnalyst" in node_names
    assert len(node_names) >= 2
