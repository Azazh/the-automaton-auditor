# Guidelines for justice.py

# 1. Implement deterministic Python logic for conflict resolution.
# 2. Define hardcoded rules for:
#    - Security Override: Security flaws cap scores at 3.
#    - Fact Supremacy: Forensic evidence overrides subjective opinions.
#    - Dissent Requirement: Summarize disagreements among judges when score variance > 2.
# 3. Ensure the ChiefJusticeNode synthesizes judge opinions into a final verdict.
# 4. Output the final AuditReport as structured Markdown for transparency.
# 5. Handle edge cases where evidence is missing or contradictory.

from langgraph.nodes import Node
from src.state import JudicialOpinion
from typing import List

class ChiefJustice(Node):
    async def run(self, opinions: List[JudicialOpinion]) -> JudicialOpinion:
        # Deterministic synthesis: If any judge scores <=2, cap the final score at 2 (Rule of Security)
        min_score = min(op.score for op in opinions)
        if min_score <= 2:
            return JudicialOpinion(
                judge="ChiefJustice",
                opinion="Security or completeness flaw detected. Verdict capped.",
                score=2
            )
        # Otherwise, average the scores (rounded)
        avg_score = round(sum(op.score for op in opinions) / len(opinions))
        return JudicialOpinion(
            judge="ChiefJustice",
            opinion="All criteria met. Verdict reflects consensus.",
            score=avg_score
        )