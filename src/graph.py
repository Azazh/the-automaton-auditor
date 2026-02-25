from langgraph import StateGraph
from src.state import AgentState
from src.nodes.detectives import RepoInvestigator, DocAnalyst, VisionInspector
from langgraph.nodes import Node
from src.nodes.judges import Prosecutor, Defense, TechLead
from src.nodes.justice import ChiefJustice

class EvidenceAggregator(Node):
    async def run(self, evidences: dict) -> dict:
        """
        Aggregate evidence from multiple sources and validate keys.

        Args:
            evidences (dict): The collected evidence dictionary.

        Returns:
            dict: The aggregated evidence dictionary.
        """
        required_keys = {"graph_structure", "git_narrative", "pdf_analysis", "image_analysis"}
        missing_keys = required_keys - evidences.keys()

        if missing_keys:
            evidences["error"] = {
                "rationale": f"Missing keys: {missing_keys}",
                "confidence": 0.0,
                "source": "EvidenceAggregator"
            }
        return evidences

class ErrorNode(Node):
    async def run(self, state: dict) -> dict:
        """
        Handle errors in the graph execution.

        Args:
            state (dict): The current state.

        Returns:
            dict: The updated state with error information.
        """
        state["error"] = {
            "rationale": "Invalid input detected.",
            "confidence": 0.0,
            "source": "ErrorNode"
        }
        return state

# Initialize the StateGraph
graph = StateGraph(AgentState)

# Define nodes
repo_investigator = RepoInvestigator()
doc_analyst = DocAnalyst()
vision_inspector = VisionInspector()
evidence_aggregator = EvidenceAggregator()
error_node = ErrorNode()

# Judicial Layer nodes
prosecutor = Prosecutor()
defense = Defense()
tech_lead = TechLead()
chief_justice = ChiefJustice()

# Define graph wiring
graph.add_fan_out("START", [repo_investigator, doc_analyst, vision_inspector])
graph.add_fan_in([repo_investigator, doc_analyst, vision_inspector], evidence_aggregator)

# Fan-out to all judges in parallel after aggregation
graph.add_fan_out(evidence_aggregator, [prosecutor, defense, tech_lead])
graph.add_fan_in([prosecutor, defense, tech_lead], chief_justice)

graph.add_edge(chief_justice, error_node)