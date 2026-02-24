from typing import List, Optional, Dict, Annotated
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
import operator

# --- Detective Output ---
class Evidence(BaseModel):
    goal: str = Field(..., description="The objective of the evidence collection")
    found: bool = Field(..., description="Whether the artifact exists")
    content: Optional[str] = Field(None, description="The content of the evidence, if applicable")
    location: str = Field(..., description="File path or commit hash")
    rationale: str = Field(..., description="Rationale for confidence in the evidence")
    confidence: float = Field(..., description="Confidence level in the evidence (0-1)")

# --- Judge Output ---
class JudicialOpinion(BaseModel):
    judge: str = Field(..., description="The role of the judge (Prosecutor, Defense, TechLead)")
    criterion_id: str = Field(..., description="The rubric criterion being evaluated")
    score: int = Field(..., description="Score assigned by the judge")
    argument: str = Field(..., description="The reasoning behind the score")
    cited_evidence: List[str] = Field(..., description="List of evidence IDs cited in the argument")

# --- Chief Justice Output ---
class CriterionResult(BaseModel):
    dimension_id: str
    dimension_name: str
    final_score: int = Field(..., description="Final score for the criterion")
    judge_opinions: List[JudicialOpinion]
    dissent_summary: Optional[str] = Field(None, description="Summary of dissent among judges")
    remediation: str = Field(..., description="File-level remediation instructions")

class AuditReport(BaseModel):
    repo_url: str
    executive_summary: str
    overall_score: float
    criteria: List[CriterionResult]
    remediation_plan: str

# --- Graph State ---
class AgentState(TypedDict):
    repo_url: str
    pdf_path: str
    rubric_dimensions: List[Dict]
    evidences: Annotated[Dict[str, List[Evidence]], operator.ior]
    opinions: Annotated[List[JudicialOpinion], operator.add]
    final_report: AuditReport