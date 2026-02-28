import json
import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from pydantic import ValidationError
from src.state import JudicialOpinion, Evidence
from src.utils.llm_provider import LLMProvider
import json as _json
# Load rubric for persona prompts
def load_rubric():
    rubric_path = os.path.join(os.path.dirname(__file__), '../../rubric/week2_rubric.json')
    with open(rubric_path, 'r') as f:
        return json.load(f)

RUBRIC = load_rubric()
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
    return [d for d in RUBRIC["dimensions"] if d["target_artifact"] == "github_repo"]

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

    print(f"[{persona}] Judge node starting.")
    opinions = state.get("opinions", [])
    tasks = get_judge_tasks()
    llm = LLMProvider(provider="groq") 
    for task in tasks:
        criterion_id = task["id"]
        evidence = get_evidence(state, criterion_id)
        evidence_str = "\n".join([
            f"- {ev.location}: {ev.content}" for ev in evidence
        ]) if evidence else "No evidence found."
        user_prompt = (
            f"You are the {persona} in a digital courtroom.\n"
            f"Criterion: {criterion_id}\n"
            f"Persona Instructions: {prompt}\n"
            f"Evidence (with file paths):\n{evidence_str}\n"
            "Return your verdict as a JSON object with keys: score (1-5 int), argument (str), cited_evidence (list of file paths you are citing, e.g. ['src/state.py', 'src/graph.py']).\n"
            "Example JSON: {\"score\": 3, \"argument\": \"The state is well-typed but lacks reducers.\", \"cited_evidence\": [\"src/state.py\"]}"
        )
        messages = [
            {"role": "system", "content": "You are a helpful, precise, and honest digital judge. Always return valid JSON."},
            {"role": "user", "content": user_prompt}
        ]
        for attempt in range(3):
            try:
                response = llm.chat(messages, temperature=0.2, max_tokens=512)
                # Extract JSON from response
                if '{' in response:
                    start = response.index('{')
                    end = response.rindex('}') + 1
                    json_str = response[start:end]
                    data = _json.loads(json_str)
                else:
                    raise ValueError("No JSON object in LLM response.")
                opinion = JudicialOpinion(
                    judge=persona,
                    criterion_id=criterion_id,
                    score=int(data.get("score", 1)),
                    argument=data.get("argument", "No argument provided."),
                    cited_evidence=data.get("cited_evidence", [])
                )
                opinion = JudicialOpinion.parse_obj(opinion.dict())
                print(f"[{persona}] Output: {opinion}")
                opinions.append(opinion)
                break
            except (ValidationError, Exception) as ve:
                print(f"[{persona}] Output validation failed: {ve}. Retrying...")
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
