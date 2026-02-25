from langgraph.nodes import Node
from src.state import Evidence, JudicialOpinion
from datetime import datetime
from typing import Dict, Any

class Prosecutor(Node):
    async def run(self, evidences: Dict[str, Evidence]) -> JudicialOpinion:
        # Example: Penalize missing forensic_signature or low confidence
        for key, ev in evidences.items():
            if not ev.forensic_signature or ev.confidence < 0.5:
                return JudicialOpinion(
                    judge="Prosecutor",
                    opinion=f"Evidence {key} is weak or unverifiable.",
                    score=2
                )
        return JudicialOpinion(
            judge="Prosecutor",
            opinion="All evidence meets minimum prosecutorial standards.",
            score=5
        )

class Defense(Node):
    async def run(self, evidences: Dict[str, Evidence]) -> JudicialOpinion:
        # Example: Reward high confidence and rationale
        for key, ev in evidences.items():
            if ev.confidence > 0.8 and ev.rationale:
                return JudicialOpinion(
                    judge="Defense",
                    opinion=f"Evidence {key} is robust and well-justified.",
                    score=5
                )
        return JudicialOpinion(
            judge="Defense",
            opinion="Some evidence lacks strong justification.",
            score=3
        )

class TechLead(Node):
    async def run(self, evidences: Dict[str, Evidence]) -> JudicialOpinion:
        # Example: Check for analysis_timestamp recency
        now = datetime.utcnow().isoformat()
        for key, ev in evidences.items():
            if not ev.analysis_timestamp:
                return JudicialOpinion(
                    judge="TechLead",
                    opinion=f"Evidence {key} missing analysis timestamp.",
                    score=2
                )
        return JudicialOpinion(
            judge="TechLead",
            opinion="All evidence is recent and timestamped.",
            score=5
        )
