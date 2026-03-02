from typing import Dict, Any, List, Tuple
import os
import json
from typing import Dict, Any, List
from src.state import JudicialOpinion, CriterionResult, AuditReport
from statistics import variance, mean


def load_rubric():
    rubric_path = os.path.join(os.path.dirname(__file__), '../../rubric/week2_rubric.json')
    with open(rubric_path, 'r') as f:
        return json.load(f)

# Load synthesis rules from file for fallback
SYNTHESIS_RULES_FROM_FILE = load_rubric().get("synthesis_rules", {})

def get_rubric_from_state(state: Dict[str, Any]) -> dict:
    # Use rubric_dimensions from state if present, else fallback to file
    if "rubric_dimensions" in state and state["rubric_dimensions"]:
        return {"dimensions": state["rubric_dimensions"], "synthesis_rules": SYNTHESIS_RULES_FROM_FILE}
    else:
        return load_rubric()

def get_remediation_for_criterion(criterion_id: str) -> str:
    # Placeholder: In a real system, this would be more sophisticated
    return f"Review and improve code for criterion: {criterion_id}."

def summarize_dissent(opinions: List[JudicialOpinion]) -> str:
    # Summarize why judges disagreed, referencing all arguments and cited evidence
    if not opinions or len(opinions) < 2:
        return ""
    summary = ["Dissent detected due to high score variance:"]
    for op in opinions:
        summary.append(f"- {op.judge}: Score {op.score}\n  Argument: {op.argument}\n  Cited Evidence: {', '.join(op.cited_evidence)}")
    summary.append("This wide disagreement reflects conflicting interpretations of the evidence and rubric. See above for details.")
    return "\n".join(summary)

def apply_synthesis_rules(criterion_id, opinions: List[JudicialOpinion], evidences: Dict[str, Any]) -> Tuple[int, str]:
    # Rule 1: Security override
    if criterion_id == "safe_tool_engineering":
        for op in opinions:
            if op.judge == "Prosecutor" and "security" in op.argument.lower():
                return min(3, min(op.score for op in opinions)), "Security override applied."
    # Rule 2: Fact supremacy
    if criterion_id == "state_management_rigor":
        for op in opinions:
            if op.judge == "Defense" and "deep metacognition" in op.argument.lower():
                # Check detective evidence for missing artifact
                found = any(ev.found for evs in evidences.values() for ev in evs if hasattr(ev, "goal") and "state" in ev.goal.lower())
                if not found:
                    return min(op.score for op in opinions), "Fact supremacy: Defense overruled."
    # Rule 3: Functionality weight
    if criterion_id == "graph_orchestration":
        for op in opinions:
            if op.judge == "TechLead" and "modular" in op.argument.lower():
                return op.score, "Functionality weight: TechLead confirmed modularity."
    return round(mean([op.score for op in opinions])), "Standard synthesis."

def compute_variance(opinions: List[JudicialOpinion]) -> float:
    scores = [op.score for op in opinions]
    return variance(scores) if len(scores) > 1 else 0.0
def render_agentstate_fields(state: dict) -> str:
        """Render all AgentState fields and their values for explicit report inclusion."""
        lines = ["\n---\n## AgentState Fields (Full State Snapshot)\n"]
        lines.append(f"- repo_url: {state.get('repo_url','')}")
        lines.append(f"- pdf_path: {state.get('pdf_path','')}")
        lines.append(f"- rubric_dimensions: {state.get('rubric_dimensions','')}")
        evidences = state.get('evidences',{})
        lines.append(f"- evidences (keys): {list(evidences.keys())}")
        opinions = state.get('opinions',[])
        lines.append(f"- opinions (count): {len(opinions)}")
        lines.append(f"- final_report: {'present' if state.get('final_report') else 'missing'}")
        return "\n".join(lines)

def render_markdown_report(report: AuditReport) -> str:
    md = [f"# Audit Report for `{report.repo_url}`"]
    md.append("\n---\n## 📝 AuditReport Model Fields\n")
    md.append(f"**repo_url:** `{report.repo_url}`  ")
    md.append(f"**executive_summary:** {report.executive_summary}  ")
    md.append(f"**overall_score:** `{report.overall_score}`  ")
    md.append(f"**remediation_plan:** {report.remediation_plan}  ")
    md.append(f"**criteria (count):** `{len(report.criteria)}`  ")
    md.append("\n---\n## 🏆 Executive Summary\n")
    md.append(f"> {report.executive_summary}")
    md.append("\n---\n## 📊 Criterion Breakdown\n")
    for crit in report.criteria:
        md.append(f"\n### {crit.dimension_name}  ")
        md.append(f"**Score:** `{crit.final_score}`  ")
        md.append(f"**Criterion ID:** `{crit.dimension_id}`  ")
        md.append(f"**Remediation:** {crit.remediation}  ")
        if crit.dissent_summary:
            md.append(f"**Dissent:**\n> {crit.dissent_summary}\n")
        md.append(f"**Judge Opinions:**")
        for op in crit.judge_opinions:
            md.append(f"- **{op.judge}**  ")
            md.append(f"  - Score: `{op.score}`  ")
            md.append(f"  - Argument: {op.argument}")
            if op.cited_evidence and any(e.strip() for e in op.cited_evidence):
                md.append(f"  - Cited Evidence: {', '.join([e for e in op.cited_evidence if e.strip()])}")
            else:
                md.append(f"  - Cited Evidence: None")
    md.append(f"\n---\n## 🛠️ Remediation Plan\n{report.remediation_plan}\n")
    return "\n".join(md)

 

async def chief_justice(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    ChiefJusticeNode: Synthesizes all judge opinions using deterministic rules. Generates a Markdown report.
    """
    print("[ChiefJustice] Synthesizing final verdict.")
    opinions = state.get("opinions", [])
    evidences = state.get("evidences", {})
    rubric_bundle = get_rubric_from_state(state)
    rubric = rubric_bundle["dimensions"]
    criteria_results = []
    total_score = 0
    for dim in rubric:
        criterion_id = dim["id"]
        criterion_name = dim["name"]
        relevant_ops = [op for op in opinions if op.criterion_id == criterion_id]
        if not relevant_ops:
            continue
        scores = [op.score for op in relevant_ops]
        score_variance = max(scores) - min(scores) if len(scores) > 1 else 0
        dissent = summarize_dissent(relevant_ops) if score_variance > 2 else None
        final_score, rule_applied = apply_synthesis_rules(criterion_id, relevant_ops, evidences)
        total_score += final_score
        remediation = get_remediation_for_criterion(criterion_id)
        criteria_results.append(CriterionResult(
            dimension_id=criterion_id,
            dimension_name=criterion_name,
            final_score=final_score,
            judge_opinions=relevant_ops,
            dissent_summary=dissent,
            remediation=remediation
        ))
    overall_score = round(total_score / len(criteria_results), 2) if criteria_results else 0.0
    executive_summary = f"Final audit complete. Aggregate score: {overall_score}. See breakdown below."
    remediation_plan = "\n".join([c.remediation for c in criteria_results])
    report = AuditReport(
        repo_url=state.get("repo_url", ""),
        executive_summary=executive_summary,
        overall_score=overall_score,
        criteria=criteria_results,
        remediation_plan=remediation_plan
    )
    # Write Markdown report to correct location (self or peer)
    peer_repo_url = os.environ.get("PEER_REPO_URL")
    if peer_repo_url and report.repo_url.strip().lower() == peer_repo_url.strip().lower():
        output_dir = os.path.join(os.path.dirname(__file__), '../../audit/report_onpeer_generated')
    else:
        output_dir = os.path.join(os.path.dirname(__file__), '../../audit/report_onself_generated')
        
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'audit_report.md')
    with open(output_path, 'w') as f:
        f.write(render_markdown_report(report))
        f.write(render_agentstate_fields(state))
    print(f"[ChiefJustice] Markdown report written to {output_path}")
    state["final_report"] = report
    return state
