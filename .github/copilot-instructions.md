# AI Commandments for the Automaton Auditor
> Enforced Engineering Governance Rules for Copilot Agent

This document defines mandatory behavioral, architectural, and governance rules for the Automaton Auditor system.  
Copilot must treat these as non-optional constraints.

---

# References to Standards and Governance

The following documents provide additional rules, standards, and governance protocols that must be adhered to in the Automaton Auditor project:

1. **Code Style Standards**
   - Location: `docs/standards/code_style.md`
   - Description: Defines the technical law for the project, including Pydantic rigor, parallel state management, strict typing, asynchronous patterns, and separation of concerns.

2. **CI Pipeline Specification**
   - Location: `docs/standards/ci_pipeline_spec.md`
   - Description: Details the GitHub Actions CI pipeline stages, including forensic scans, typing validation, judicial integrity tests, and elite-tier checks like LangSmith integration and Git narrative validation.

3. **Testing SOP**
   - Location: `docs/standards/testing_sop.md`
   - Description: Outlines the standard operating procedures for testing, including unit, integration, and adversarial tests.

4. **Git Protocol**
   - Location: `docs/standards/git_protocol.md`
   - Description: Specifies the rules for Git workflows, including branch naming conventions, commit message standards, and pull request guidelines.

5. **Self-Improvement Documentation**
   - Location: `audit/SELF_IMPROVEMENT.md`
   - Description: Tracks how peer feedback and iterative improvements enhance the detection logic and overall project quality.

---

# 1. CORE PHILOSOPHY — FROM GENERATION TO GOVERNANCE

## Rule 1.1 — Metacognition First
Copilot MUST always prioritize the "Auditor" mindset.  
Generated code must:
- Evaluate
- Verify
- Document **why** a specific engineering choice was made

Code that only executes without verification is non-compliant.

## Rule 1.2 — Master Thinker Standard
Every implementation MUST aim for **Score 5 (Master Thinker)** by ensuring:
- Deep verification
- Deterministic synthesis
- Actionable remediation plans

---

# 2. ARCHITECTURE & ORCHESTRATION (LangGraph Strictness)

## Rule 2.1 — Hierarchical State Graph
All workflows MUST follow the three-layer structure:

Forensic Layer (Detectives)  
→ Judicial Layer (Judges)  
→ Synthesis Layer (Supreme Court)

Any deviation is a violation.

## Rule 2.2 — Parallel Execution Requirement
Detectives and Judges MUST:
- Run in parallel
- Use LangGraph fan-out/fan-in patterns

Linear sequencing of these layers is defined as:
> "Orchestration Fraud"

## Rule 2.3 — Pydantic Rigor
Every node output and state transition MUST:
- Use Pydantic models

Unstructured dict outputs are prohibited.

## Rule 2.4 — State Reducers
Parallel state updates MUST use:
- `Annotated` with `operator.add` for lists
- `Annotated` with `operator.ior` for dictionaries

This prevents evidence overwrites.

---

# 3. FORENSIC PROTOCOL (Detective Layer)

## Rule 3.1 — Structural Over Textual
Detectives MUST prioritize:
- Abstract Syntax Tree (AST) analysis

Example validations:
- Class inherits from `BaseModel`
- Graph is wired correctly

Text-based pattern matching alone is insufficient.

## Rule 3.2 — Security Sandboxing
Any repository interaction MUST use:
- `tempfile.TemporaryDirectory`

No direct filesystem contamination allowed.

## Rule 3.3 — No Security Negligence
Forbidden:
- Raw `os.system` calls

Required:
- `subprocess` module
- Proper argument sanitization

## Rule 3.4 — Evidence Formatting
Detectives MUST:
- Return objective
- Structured JSON evidence

Detectives are strictly forbidden from:
- Expressing opinions
- Giving “vibe” assessments

---

# 4. JUDICIAL DIALECTICS (The Bench)

## Rule 4.1 — Persona Integrity
The following roles MUST have strictly separate system prompts:
- Prosecutor
- Defense
- Tech Lead

Shared prompts are prohibited.

## Rule 4.2 — Prevent Persona Collusion
Judges MUST:
- Not agree by default
- Be prompted to find conflicting interpretations

Example dialectic:
- “Innovative” vs. “Messy”

## Rule 4.3 — Structured Scoring
All judges MUST output:
- Score (1–5)
- A "Citation" linking to specific Detective evidence

No score without citation.

---

# 5. SUPREME COURT SYNTHESIS (Final Verdict)

## Rule 5.1 — Deterministic Justice
The ChiefJusticeNode MUST NOT:
- Be a simple LLM summary

It MUST:
- Implement hardcoded Python conflict-resolution logic

Example:
If a security flaw is detected → Maximum possible score = 2

## Rule 5.2 — The "Why" Factor
The final report MUST:
- Explain why a judge was overruled
- Reference the "Statute of Engineering" (rubric)

---

# 6. NON-TECHNICAL GOVERNANCE & PROCESS

## Rule 6.1 — Git Narrative
Copilot MUST suggest commit messages that:
- Follow Conventional Commits
  - `feat:`
  - `fix:`
  - `docs:`
- Reflect forensic progression:
  - Scaffolding → Forensic Tools → Judicial Logic

## Rule 6.2 — ADR Documentation
When proposing major architectural changes:
Copilot MUST suggest creating an:
- Architecture Decision Record (ADR)
- Location: `docs/ADR/`

## Rule 6.3 — MinMax Optimization
Copilot MUST remind the developer to document:
- How peer feedback improved detection logic
- File: `audit/SELF_IMPROVEMENT.md`

## Rule 6.4 — Test-First Requirement

### Detectives
Must test against:
- "Broken" repo structures
- "Correct" repo structures

### Judges
Must test against:
- "Golden Evidence"

Ensures persona bias integrity.

---

# 7. PROHIBITED PATTERNS (Score 1–2 Traps)

## Rule 7.1 — No "Vibe Coding"
Forbidden phrases:
- "I think the code is good"

Required evidence-based language:
- "Evidence shows 100% test coverage"
- "AST analysis confirms circular dependencies"

## Rule 7.2 — No Monolithic Nodes
If a node performs both:
- Finding
- Judging

It MUST be split.

## Rule 7.3 — No Hardcoded Secrets
Secrets MUST:
- Use `.env`
- Use `python-dotenv`

Hardcoded credentials are prohibited.

---

# ENFORCEMENT CLAUSE

If a generated implementation violates any rule above:
- It MUST be refactored before approval.
- Compliance takes priority over speed.
- Determinism takes priority over elegance.