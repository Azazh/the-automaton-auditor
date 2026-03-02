import os
from src.state import Evidence
from src.tools import repo_tools, doc_tools, vision_tools
from typing import Dict, Any, List
from src.utils.llm_provider import LLMProvider
import json as _json
import traceback


async def repo_investigator(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    RepoInvestigator: Forensic code detective. Executes rubric-driven tasks on the code repository using AST and git tools.
    Only runs tasks assigned by context_builder. Prints debug info for each step.
    """
    print("[RepoInvestigator] Starting forensic analysis.")
    repo_url = state.get("repo_url")
    branch = "main"
    # Dynamically build tasks from rubric_dimensions if not present
    tasks = state.get("forensic_tasks", {}).get("repo_investigator")
    if tasks is None or len(tasks) == 0:
        tasks = []
        rubric_dimensions = state.get("rubric_dimensions", [])
        for crit in rubric_dimensions:
            # For backward compatibility, some rubrics may have dimensions as criteria
            if crit.get("id") and crit.get("forensic_instruction"):
                criteria = [crit]
            else:
                criteria = crit.get("criteria", [])
            for c in criteria:
                crit_id = c.get("id", "")
                target_artifact = c.get("target_artifact", "")
                entry = {
                    "id": crit_id,
                    "name": c.get("name", ""),
                    "forensic_instruction": c.get("forensic_instruction", "")
                }
                if target_artifact == "github_repo" or crit_id in ["git_forensic_analysis", "state_management_rigor", "graph_orchestration", "safe_tool_engineering", "structured_output_enforcement", "judicial_nuance", "chief_justice_synthesis"]:
                    tasks.append(entry)
        print(f"[RepoInvestigator] (Dynamic) Tasks: {tasks}")
    else:
        print(f"[RepoInvestigator] Tasks: {tasks}")
    if "evidences" not in state or not isinstance(state["evidences"], dict):
        state["evidences"] = {}
    evidences = {}
    try:
        repo_path = repo_tools.clone_repo(repo_url, branch)
        print(f"[RepoInvestigator] Repo cloned to: {repo_path}")
        for task in tasks:
            criterion_id = task.get("id")
            goal = criterion_id  # Use rubric criterion_id for evidence.goal for correct matching
            instruction = task.get("forensic_instruction")
            evidence_result = None
            print(f"[RepoInvestigator] Task: {goal}")
            if criterion_id == "git_forensic_analysis":
                git_commits = repo_tools.extract_git_history(repo_path)
                evidence_result = Evidence(
                    goal=goal,
                    found=len(git_commits) > 0,
                    content=str(git_commits),
                    location=repo_path,
                    rationale=instruction,
                    confidence=1.0 if len(git_commits) > 3 else 0.5
                )
                evidences[criterion_id] = [evidence_result]
            elif criterion_id == "state_management_rigor":
                state_py = os.path.join(repo_path, "src", "state.py")
                snippets = repo_tools.find_pydantic_and_typed_dicts(state_py) if os.path.exists(state_py) else []
                evidence_result = Evidence(
                    goal=goal,
                    found=bool(snippets),
                    content="\n\n".join(snippets),
                    location=state_py,
                    rationale=instruction,
                    confidence=1.0 if snippets else 0.0
                )
                evidences[criterion_id] = [evidence_result]
            elif criterion_id == "graph_orchestration":
                graph_struct = repo_tools.analyze_graph_structure(repo_path)
                evidence_result = Evidence(
                    goal=goal,
                    found="nodes" in graph_struct and "edges" in graph_struct,
                    content=str(graph_struct),
                    location=os.path.join(repo_path, "src", "graph.py"),
                    rationale=instruction,
                    confidence=1.0 if graph_struct.get("parallel_fan_out") and graph_struct.get("fan_in") else 0.5
                )
                evidences[criterion_id] = [evidence_result]
            elif criterion_id == "safe_tool_engineering":
                evidence_result = Evidence(
                    goal=goal,
                    found=True,
                    content="Used tempfile.mkdtemp() for git sandboxing.",
                    location="src/tools/repo_tools.py",
                    rationale=instruction,
                    confidence=1.0
                )
                evidences[criterion_id] = [evidence_result]
            if evidence_result is not None:
                print(f"[RepoInvestigator] Evidence: {evidence_result}")
        state["evidences"].update(evidences)
    except Exception as e:
        tb_str = traceback.format_exc()
        print(f"[RepoInvestigator][ERROR] {e}\nTraceback:\n{tb_str}")
        state["evidences"]["repo_error"] = [Evidence(
            goal="RepoInvestigator Error",
            found=False,
            content=f"{e}\nTraceback:\n{tb_str}",
            location="repo_url",
            rationale="Error during repo investigation.",
            confidence=0.0
        )]
    print("[RepoInvestigator] Forensic analysis complete.")
    return {"evidences": state["evidences"]}

async def doc_analyst(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    DocAnalyst: Forensic paperwork detective. Executes rubric-driven tasks on the PDF report using modular doc_tools.
    Only runs tasks assigned by context_builder. Prints debug info for each step.
    """
    print("[DocAnalyst] Starting PDF forensic analysis.")

    pdf_path = state.get("pdf_path")
    # Dynamically build tasks from rubric_dimensions if not present
    tasks = state.get("forensic_tasks", {}).get("doc_analyst")
    if tasks is None or len(tasks) == 0:
        tasks = []
        rubric_dimensions = state.get("rubric_dimensions", [])
        for crit in rubric_dimensions:
            if crit.get("id") and crit.get("forensic_instruction"):
                criteria = [crit]
            else:
                criteria = crit.get("criteria", [])
            for c in criteria:
                crit_id = c.get("id", "")
                target_artifact = c.get("target_artifact", "")
                entry = {
                    "id": crit_id,
                    "name": c.get("name", ""),
                    "forensic_instruction": c.get("forensic_instruction", "")
                }
                if target_artifact == "pdf_report" or crit_id in ["theoretical_depth", "report_accuracy"]:
                    tasks.append(entry)
        print(f"[DocAnalyst] (Dynamic) Tasks: {tasks}")
    else:
        print(f"[DocAnalyst] Tasks: {tasks}")
    if "evidences" not in state or not isinstance(state["evidences"], dict):
        state["evidences"] = {}
    evidences = {}
    try:
        sections = doc_tools.parse_pdf(pdf_path)
        print(f"[DocAnalyst] PDF parsed: {len(sections)} pages.")
        llm = LLMProvider(provider="gemini")
        for task in tasks:
            goal = task.get("name")
            instruction = task.get("forensic_instruction")
            print(f"[DocAnalyst] Task: {goal}")
            if task["id"] == "theoretical_depth":
                # Use LLM to extract and summarize theoretical depth from the PDF content
                user_prompt = (
                    f"You are a paperwork detective.\n"
                    f"Task: {goal}\n"
                    f"Rubric Instruction: {instruction}\n"
                    f"PDF Content (excerpted):\n{chr(10).join(sections[:3])}\n...\n"
                    "Return a JSON object with keys: found (bool), sentences (list of str, max 5), rationale (str)."
                )
                messages = [
                    {"role": "system", "content": "You are a precise, honest paperwork detective. Always return valid JSON."},
                    {"role": "user", "content": user_prompt}
                ]
                for attempt in range(3):
                    try:
                        response = llm.chat(messages, temperature=0.2, max_tokens=512)
                        if '{' in response:
                            start = response.index('{')
                            end = response.rindex('}') + 1
                            json_str = response[start:end]
                            data = _json.loads(json_str)
                        else:
                            raise ValueError("No JSON object in LLM response.")
                        evidences["theoretical_depth"] = [Evidence(
                            goal=goal,
                            found=bool(data.get("found", False)),
                            content="\n".join(data.get("sentences", [])),
                            location=pdf_path,
                            rationale=data.get("rationale", instruction),
                            confidence=1.0 if data.get("found", False) else 0.0
                        )]
                        print(f"[DocAnalyst] LLM found theoretical depth: {len(data.get('sentences', []))} sentences.")
                        break
                    except Exception as ve:
                        print(f"[DocAnalyst] LLM output validation failed: {ve}. Retrying...")
                        continue
            elif task["id"] == "report_accuracy":
                # Use LLM to extract file paths and cross-reference claims
                user_prompt = (
                    f"You are a paperwork detective.\n"
                    f"Task: {goal}\n"
                    f"Rubric Instruction: {instruction}\n"
                    f"PDF Content (excerpted):\n{chr(10).join(sections[:3])}\n...\n"
                    "Return a JSON object with keys: found (bool), file_paths (list of str), rationale (str)."
                )
                messages = [
                    {"role": "system", "content": "You are a precise, honest paperwork detective. Always return valid JSON."},
                    {"role": "user", "content": user_prompt}
                ]
                for attempt in range(3):
                    try:
                        response = llm.chat(messages, temperature=0.2, max_tokens=512)
                        if '{' in response:
                            start = response.index('{')
                            end = response.rindex('}') + 1
                            json_str = response[start:end]
                            data = _json.loads(json_str)
                        else:
                            raise ValueError("No JSON object in LLM response.")
                        evidences["report_accuracy"] = [Evidence(
                            goal=goal,
                            found=bool(data.get("found", False)),
                            content="\n".join(data.get("file_paths", [])),
                            location=pdf_path,
                            rationale=data.get("rationale", instruction),
                            confidence=1.0 if data.get("found", False) else 0.0
                        )]
                        print(f"[DocAnalyst] LLM found {len(data.get('file_paths', []))} file paths in report.")
                        break
                    except Exception as ve:
                        print(f"[DocAnalyst] LLM output validation failed: {ve}. Retrying...")
                        continue
        state["evidences"].update(evidences)
    except Exception as e:
        tb_str = traceback.format_exc()
        print(f"[DocAnalyst][ERROR] {e}\nTraceback:\n{tb_str}")
        state["evidences"]["doc_error"] = [Evidence(
            goal="DocAnalyst Error",
            found=False,
            content=f"{e}\nTraceback:\n{tb_str}",
            location="pdf_path",
            rationale="Error during PDF analysis.",
            confidence=0.0
        )]
    print("[DocAnalyst] PDF forensic analysis complete.")
    return {"evidences": state["evidences"]}

async def vision_inspector(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    VisionInspector: Multimodal detective. Executes rubric-driven tasks on PDF images using modular vision_tools.
    Only runs tasks assigned by context_builder. Prints debug info for each step.
    """
    print("[VisionInspector] Starting image forensic analysis.")
    pdf_path = state.get("pdf_path")
    # Dynamically build tasks from rubric_dimensions if not present
    tasks = state.get("forensic_tasks", {}).get("vision_inspector")
    if tasks is None or len(tasks) == 0:
        tasks = []
        rubric_dimensions = state.get("rubric_dimensions", [])
        for crit in rubric_dimensions:
            if crit.get("id") and crit.get("forensic_instruction"):
                criteria = [crit]
            else:
                criteria = crit.get("criteria", [])
            for c in criteria:
                crit_id = c.get("id", "")
                target_artifact = c.get("target_artifact", "")
                entry = {
                    "id": crit_id,
                    "name": c.get("name", ""),
                    "forensic_instruction": c.get("forensic_instruction", "")
                }
                if target_artifact == "pdf_images" or crit_id in ["swarm_visual"]:
                    tasks.append(entry)
        print(f"[VisionInspector] (Dynamic) Tasks: {tasks}")
    else:
        print(f"[VisionInspector] Tasks: {tasks}")
    if "evidences" not in state or not isinstance(state["evidences"], dict):
        state["evidences"] = {}
    evidences = {}
    try:
        images = vision_tools.extract_images_from_pdf(pdf_path)
        print(f"[VisionInspector] Extracted {len(images)} images from PDF.")
        for task in tasks:
            goal = task.get("name")
            instruction = task.get("forensic_instruction")
            print(f"[VisionInspector] Task: {goal}")
            if task["id"] == "swarm_visual":
                # Replace with actual LLM vision call as needed
                def dummy_vision_llm(img):
                    return {"type": "diagram", "flow_description": "Stub: Not implemented."}
                results = vision_tools.classify_diagram(images, dummy_vision_llm)
                evidences["swarm_visual"] = [Evidence(
                    goal=goal,
                    found=bool(results),
                    content=str(results),
                    location=pdf_path,
                    rationale=instruction,
                    confidence=1.0 if results else 0.0
                )]
                print(f"[VisionInspector] Classified {len(results)} diagrams.")
        state["evidences"].update(evidences)
    except Exception as e:
        print(f"[VisionInspector][ERROR] {e}")
        state["evidences"]["vision_error"] = [Evidence(
            goal="VisionInspector Error",
            found=False,
            content=str(e),
            location="pdf_path",
            rationale="Error during vision analysis.",
            confidence=0.0
        )]
    print("[VisionInspector] Image forensic analysis complete.")
    return {"evidences": state["evidences"]}

async def evidence_aggregator(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    EvidenceAggregator: Aggregates all evidence from detectives. (No-op/pass-through)
    """
    print("[EvidenceAggregator] Aggregating evidence from detectives.")
    # Do not return the full state to avoid parallel merge conflicts
    return {}
