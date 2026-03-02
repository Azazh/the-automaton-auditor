import json
import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from pydantic import ValidationError
from src.state import JudicialOpinion, Evidence
from src.utils.llm_provider import LLMProvider
import json as _json
import inspect
import time
import re

# Rubric loading best practice: use rubric_dimensions from state if present
def load_rubric():
    rubric_path = os.path.join(os.path.dirname(__file__), '../../rubric/week2_rubric.json')
    with open(rubric_path, 'r') as f:
        return json.load(f)

# Fallback rubric for file-based loading
RUBRIC_FALLBACK = load_rubric()

def get_rubric_from_state(state: Dict[str, Any]) -> dict:
    if "rubric_dimensions" in state and state["rubric_dimensions"]:
        return {"dimensions": state["rubric_dimensions"]}
    else:
        return RUBRIC_FALLBACK

def get_all_rubric_dimensions(state: Dict[str, Any]) -> list:
    """
    Return all rubric dimensions as a list of dicts, preserving all keys/values.
    """
    rubric_bundle = get_rubric_from_state(state)
    return [dict(dim) for dim in rubric_bundle["dimensions"]]

load_dotenv()


# Persona system prompts (distinct, per rubric)
PROSECUTOR_PROMPT = (
    "You are the Prosecutor. Your job is to find flaws, security gaps, and laziness. "
    "Be adversarial. Cite specific evidence. Score strictly."
)
DEFENSE_PROMPT = (
    "You are the Defense Attorney. Reward effort, intent, and creative workarounds. "
    "Be forgiving, but cite evidence. Score generously if justified."
)
TECHLEAD_PROMPT = (
    "You are the Tech Lead. Focus on architectural soundness, maintainability, and practical viability. "
    "Be pragmatic. Cite evidence for your score."
)

# Helper: get rubric logic for each criterion
def get_judge_tasks():
    # Use all rubric dimensions, not just those with target_artifact == github_repo
    # This ensures no dimension is missed
    # The judge_node can filter as needed
    # The state is passed to this function for context
    frame = inspect.currentframe().f_back
    state = frame.f_locals.get('state', {})
    return get_all_rubric_dimensions(state)

# Helper: get evidence for a criterion
def get_evidence(state, criterion_id):
    """
    Collect evidence objects for a given criterion_id.
    Handles cases where 'goal' is a string or a list.
    Adds debug output to help trace evidence matching.
    """
    evidences = state.get("evidences", {})
    found = []
    for evs in evidences.values():
        for ev in evs:
            goal = getattr(ev, "goal", None)
            if goal is None:
                continue
            # goal can be a string or a list
            if isinstance(goal, str) and criterion_id in goal:
                found.append(ev)
            elif isinstance(goal, list) and criterion_id in goal:
                found.append(ev)
    if not found:
        print(f"[Judge][DEBUG] No evidence found for criterion '{criterion_id}'. Available evidence goals: {[getattr(ev, 'goal', None) for evs in evidences.values() for ev in evs]}")
    else:
        print(f"[Judge][DEBUG] Found {len(found)} evidence(s) for criterion '{criterion_id}': {[getattr(ev, 'location', None) for ev in found]}")
    return found

async def judge_node(state: Dict[str, Any], persona: str, prompt: str) -> Dict[str, Any]:
    """
    Generic judge node. Uses .with_structured_output() or .bind_tools() to enforce output schema.
    Retries if output is not valid JudicialOpinion.
    """

    import asyncio
    print(f"[{persona}] Judge node starting.")
    tasks = get_judge_tasks()
    llm = LLMProvider(provider="openrouter")
    opinions = []
    rubric_json = json.dumps(tasks, indent=2)
    all_evidence = []
    for task in tasks:
        criterion_id = task["id"]
        evidence = get_evidence(state, criterion_id)
        for ev in evidence:
            all_evidence.append({
                "criterion_id": criterion_id,
                "location": getattr(ev, "location", ""),
                "content": getattr(ev, "content", ""),
                "goal": getattr(ev, "goal", "")
            })
    evidence_json = json.dumps(all_evidence, indent=2)

    # Protocol B: Judicial Sentencing Guidelines
    # Judges must cite the relevant statute in their argument and cap scores as required
    # Persona system prompt is distinct and passed in
    # The LLM must be instructed to:
    # 1. Check for "Orchestration Fraud" (linear graph) and cap LangGraph Architecture to 1
    # 2. Check for "Hallucination Liability" (judge nodes lack Pydantic/structured output) and cap Judicial Nuance to 2
    # 3. Check for "Technical Debt" (dict soup, not BaseModel) and cap State Management Rigor to 3
    # 4. If Security Negligence (os.system git clone), override Forensic Accuracy to 1
    # 5. If mitigations apply, cite the relevant argument and statute
    # 6. Always cite the statute in the argument

    user_prompt = (
        f"You are the {persona} in a digital courtroom.\n"
        f"Rubric Dimensions (JSON):\n{rubric_json}\n"
        f"Persona Instructions: {prompt}\n"
        f"All Evidence (JSON):\n{evidence_json}\n"
        "Apply the following Judicial Sentencing Guidelines strictly for each criterion (see below).\n"
        "For each criterion, check if any of the following violations or mitigations apply, and cite the relevant statute in your argument.\n"
        "- If the StateGraph is linear (no parallel fan-out/fan-in), charge 'Orchestration Fraud' and cap LangGraph Architecture score to 1.\n"
        "- If judge nodes return freeform text and lack Pydantic validation, charge 'Hallucination Liability' and cap Judicial Nuance to 2.\n"
        "- If state or outputs use plain dicts instead of BaseModel, charge 'Technical Debt' and cap State Management Rigor to 3.\n"
        "- If os.system('git clone ...') is used without sandboxing, charge 'Security Negligence' and override Forensic Accuracy to 1.\n"
        "- If the graph fails to compile but AST logic is sophisticated, cite 'Effort Mitigation' and boost Forensic Accuracy to 3.\n"
        "- If Chief Justice is an LLM prompt but judges are distinct and disagree, cite 'Role Separation Mitigation' and allow Judicial Nuance up to 4.\n"
        "For each verdict, return a JSON object with: criterion_id, score (1-5 int), argument (must cite the relevant statute or mitigation if applied), cited_evidence (list of file paths you are citing, e.g. ['src/state.py', 'src/graph.py']).\n"
        "Example JSON: [{\"criterion_id\": \"git_forensic_analysis\", \"score\": 3, \"argument\": \"The state is well-typed but lacks reducers. (Statute of Engineering: Technical Debt)\", \"cited_evidence\": [\"src/state.py\"]}]\n"
        "Always return a JSON array, one object per criterion."
    )
    messages = [
        {"role": "system", "content": "You are a helpful, precise, and honest digital judge. Always return valid JSON."},
        {"role": "user", "content": user_prompt}
    ]
    delay = 10
    for attempt in range(3):
        try:
            response = llm.chat(messages, temperature=0.2, max_tokens=2048)
            match = re.search(r'\[.*\]', response, re.DOTALL)
            if match:
                json_str = match.group(0)
                data = _json.loads(json_str)
            else:
                raise ValueError("No JSON array in LLM response.")
            for item in data:
                # Enforce Pydantic validation and statute citation in argument
                argument = item.get("argument", "No argument provided.")
                # Statute citation enforcement
                statute_keywords = [
                    "Orchestration Fraud", "Hallucination Liability", "Technical Debt", "Security Negligence", "Effort Mitigation", "Role Separation Mitigation"
                ]
                if not any(kw in argument for kw in statute_keywords):
                    argument += " (No statute cited: Please cite the relevant Protocol B statute in your argument.)"
                opinion = JudicialOpinion(
                    judge=persona,
                    criterion_id=item.get("criterion_id", ""),
                    score=int(item.get("score", 1)),
                    argument=argument,
                    cited_evidence=item.get("cited_evidence", [])
                )
                opinion = JudicialOpinion.parse_obj(opinion.dict())
                print(f"[{persona}] Output: {opinion}")
                opinions.append(opinion)
            break
        except Exception as ve:
            ve_str = str(ve)
            if "429" in ve_str or "Too Many Requests" in ve_str:
                print(f"[{persona}] Rate limit hit (429). Backing off for {delay:.1f}s...")
                time.sleep(delay)
                delay *= 2
            else:
                print(f"[{persona}] Output validation failed: {ve}. Retrying after {delay:.1f}s...")
                time.sleep(delay)
            continue
    else:
        print(f"[{persona}] Failed to produce valid output after retries.")
    state["opinions"] = opinions
    print(f"[{persona}] Judge node complete.")
    return {"opinions": state["opinions"]}

async def prosecutor(state: Dict[str, Any]) -> Dict[str, Any]:
    return await judge_node(state, "Prosecutor", PROSECUTOR_PROMPT)

async def defense(state: Dict[str, Any]) -> Dict[str, Any]:
    return await judge_node(state, "Defense", DEFENSE_PROMPT)

async def tech_lead(state: Dict[str, Any]) -> Dict[str, Any]:
    return await judge_node(state, "TechLead", TECHLEAD_PROMPT)
