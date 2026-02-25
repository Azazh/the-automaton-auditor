from typing import TypedDict, List, Dict, Annotated
from pydantic import BaseModel, Field
import operator

class Evidence(BaseModel):
    rationale: str = Field(description="Explanation of why this evidence is relevant.")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence level of the evidence, between 0 and 1.")
    source: str = Field(description="Source of the evidence, e.g., file name or URL.")
    raw_output: str = Field(description="The un-parsed tool result for further analysis.")
    analysis_timestamp: str = Field(description="Timestamp when the evidence was analyzed.")
    forensic_signature: str = Field(description="A unique hash or identifier for the artifact.")

class JudicialOpinion(BaseModel):
    judge: str = Field(description="Identifier for the judge issuing the opinion.")
    opinion: str = Field(description="The opinion or decision issued by the judge.")
    score: int = Field(ge=1, le=5, description="Score assigned by the judge, between 1 and 5.")

class CriterionResult(BaseModel):
    criterion: str = Field(description="The criterion being evaluated.")
    result: bool = Field(description="Whether the criterion was met.")
    details: str = Field(description="Additional details about the evaluation.")

class AuditReport(BaseModel):
    summary: str = Field(description="Summary of the audit findings.")
    findings: List[CriterionResult] = Field(description="Detailed findings of the audit.")

class AgentState(TypedDict):
    evidences: Annotated[Dict[str, Evidence], operator.ior]
    opinions: Annotated[List[JudicialOpinion], operator.add]