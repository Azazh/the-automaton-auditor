from typing import TypedDict, List, Dict, Annotated
from pydantic import BaseModel, Field
import operator

class Evidence(BaseModel):
    rationale: str = Field(description="Explanation of why this evidence is relevant.")
    source_file: str = Field(description="The specific file path where the evidence was found.")
    raw_snippet: str = Field(description="The actual code or text excerpt extracted as evidence.")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence score for this evidence, between 0 and 1.")
    verification_method: str = Field(description="The method used to verify this evidence, e.g., 'AST-Analysis', 'Docling-Parsing', 'Git-Log'.")
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
    logs: Annotated[List[str], operator.add]
    opinions: Annotated[List[JudicialOpinion], operator.add]