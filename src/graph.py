from langgraph import StateGraph
from src.state import AgentState
from src.nodes.detectives import RepoInvestigator, DocAnalyst, VisionInspector
from langgraph.nodes import Node
from src.nodes.judges import Prosecutor, Defense, TechLead
from src.nodes.justice import ChiefJustice

class LogicAggregator(Node):
    async def run(self, evidences: dict) -> dict:
        """
        Aggregate and validate completeness of evidence from all parallel detectives.
        Returns error if any required evidence is missing or if any error is present in detective outputs.
        """
        required_keys = {"graph_structure", "git_narrative", "pdf_analysis", "image_analysis"}
        missing_keys = required_keys - evidences.keys()
        error_keys = [k for k in evidences if k.startswith("error") or (isinstance(evidences[k], dict) and evidences[k].get("confidence_score", 1.0) == 0.0)]
        if missing_keys or error_keys:
            evidences["aggregation_error"] = {
                "rationale": f"Missing keys: {missing_keys}. Error keys: {error_keys}",
                "confidence_score": 0.0,
                "source_file": "LogicAggregator"
            }
        return evidences

class ErrorNode(Node):
    async def run(self, state: dict) -> dict:
        state["error"] = {
            "rationale": "Invalid input detected.",
            "confidence_score": 0.0,
            "source_file": "ErrorNode"
        }
        return state

# Initialize the StateGraph
graph = StateGraph(AgentState)

# Define nodes
repo_investigator = RepoInvestigator()
doc_analyst = DocAnalyst()
vision_inspector = VisionInspector()
logic_aggregator = LogicAggregator()
error_node = ErrorNode()

# Judicial Layer nodes
prosecutor = Prosecutor()
defense = Defense()
tech_lead = TechLead()
chief_justice = ChiefJustice()

# Define graph wiring with conditional/error routing
fan_out_detectives = [repo_investigator, doc_analyst, vision_inspector]
graph.add_fan_out("START", fan_out_detectives)
graph.add_fan_in(fan_out_detectives, logic_aggregator)

# Conditional error routing for each detective
for detective in fan_out_detectives:
    graph.add_edge(detective, error_node, condition=lambda evidences: "error" in evidences)

# Fan-out to all judges in parallel after aggregation
graph.add_fan_out(logic_aggregator, [prosecutor, defense, tech_lead])
graph.add_fan_in([prosecutor, defense, tech_lead], chief_justice)

# Route aggregation errors to error node
graph.add_edge(logic_aggregator, error_node, condition=lambda evidences: "aggregation_error" in evidences)

graph.add_edge(chief_justice, error_node)