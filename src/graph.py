from langgraph.graph import StateGraph, END
from src.state import AgentState

from src.nodes.detectives import repo_investigator, doc_analyst, vision_inspector, evidence_aggregator
from src.nodes.judges import prosecutor, defense, tech_lead
from src.nodes.justice import chief_justice

# --- Error Handling Node ---
def error_node(state):
  print("[ErrorNode] Error detected in pipeline. State:", state)
  # Optionally, set a flag or error message in state
  state["error"] = True
  return state

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

    # Error Handling Node
    graph.add_node("error_node", error_node)

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


    # Detectives → Evidence Aggregator (fan-in) with error handling
    def repo_investigator_router(state):
      if state.get("evidences", {}).get("repo_error"):
        return "error_node"
      return "evidence_aggregator"
    def doc_analyst_router(state):
      if state.get("evidences", {}).get("doc_error"):
        return "error_node"
      return "evidence_aggregator"
    def vision_inspector_router(state):
      if state.get("evidences", {}).get("vision_error"):
        return "error_node"
      return "evidence_aggregator"

    graph.add_conditional_edges("repo_investigator", repo_investigator_router)
    graph.add_conditional_edges("doc_analyst", doc_analyst_router)
    graph.add_conditional_edges("vision_inspector", vision_inspector_router)


    # Evidence Aggregator → Judges (parallel)
    graph.add_edge("evidence_aggregator", "prosecutor")
    graph.add_edge("evidence_aggregator", "defense")
    graph.add_edge("evidence_aggregator", "tech_lead")

    # Judges → Chief Justice (fan-in) with error handling
    def prosecutor_router(state):
      if state.get("error"):
        return "error_node"
      return "chief_justice"
    def defense_router(state):
      if state.get("error"):
        return "error_node"
      return "chief_justice"
    def tech_lead_router(state):
      if state.get("error"):
        return "error_node"
      return "chief_justice"

    graph.add_conditional_edges("prosecutor", prosecutor_router)
    graph.add_conditional_edges("defense", defense_router)
    graph.add_conditional_edges("tech_lead", tech_lead_router)

    # Chief Justice → END
    graph.add_edge("chief_justice", END)

    print("Graph architecture: Detectives (parallel) → Evidence Aggregator (fan-in) → Judges (parallel) → Chief Justice (synthesis) → END")
    return graph.compile()

# Export compiled graph for main.py
compiled_graph = build_graph()
