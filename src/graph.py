from langgraph.graph import StateGraph, END
from src.state import AgentState
from src.nodes.detectives import repo_investigator, doc_analyst, vision_inspector, evidence_aggregator
from src.nodes.judges import prosecutor, defense, tech_lead
from src.nodes.justice import chief_justice

def build_graph():
    """
    Build and compile the Automaton Auditor orchestration graph.
    Architecture:
      - Layer 1: Parallel Detective Fan-Out (repo_investigator, doc_analyst, vision_inspector)
      - Evidence Aggregation (evidence_aggregator)
      - Layer 2: Parallel Judicial Fan-Out (prosecutor, defense, tech_lead)
      - Synthesis (chief_justice)
      - END: Final report output
    """
    graph = StateGraph(AgentState)

    # Explicit START node for parallel fan-out
    graph.add_node("START", lambda state: state)
    graph.set_entry_point("START")

    # Layer 1: Detectives (parallel)
    graph.add_node("repo_investigator", repo_investigator)
    graph.add_node("doc_analyst", doc_analyst)
    graph.add_node("vision_inspector", vision_inspector)

    # Evidence Aggregator (fan-in)
    graph.add_node("evidence_aggregator", evidence_aggregator)

    # Layer 2: Judges (parallel)
    graph.add_node("prosecutor", prosecutor)
    graph.add_node("defense", defense)
    graph.add_node("tech_lead", tech_lead)

    # Synthesis (Chief Justice)
    graph.add_node("chief_justice", chief_justice)

    # Edges: START → Detectives (parallel)
    graph.add_edge("START", "repo_investigator")
    graph.add_edge("START", "doc_analyst")
    graph.add_edge("START", "vision_inspector")

    # Detectives → Evidence Aggregator (fan-in)
    graph.add_edge("repo_investigator", "evidence_aggregator")
    graph.add_edge("doc_analyst", "evidence_aggregator")
    graph.add_edge("vision_inspector", "evidence_aggregator")

    # Evidence Aggregator → Judges (parallel)
    graph.add_edge("evidence_aggregator", "prosecutor")
    graph.add_edge("evidence_aggregator", "defense")
    graph.add_edge("evidence_aggregator", "tech_lead")

    # Judges → Chief Justice (fan-in)
    graph.add_edge("prosecutor", "chief_justice")
    graph.add_edge("defense", "chief_justice")
    graph.add_edge("tech_lead", "chief_justice")

    # Chief Justice → END
    graph.add_edge("chief_justice", END)

    print("Graph architecture: Detectives (parallel) → Evidence Aggregator (fan-in) → Judges (parallel) → Chief Justice (synthesis) → END")
    return graph.compile()

# Export compiled graph for main.py
compiled_graph = build_graph()