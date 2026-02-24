# GitHub Actions CI Pipeline Specification

This document defines the CI pipeline for the "Automaton Auditor" project. The pipeline ensures that every commit adheres to the project's technical standards and governance protocols. Each stage is designed to enforce specific aspects of the challenge requirements and maintain the highest level of code quality.

---

## Pipeline Stages

### 1. The Forensic Scan (Security)
**Objective**: Detect and prevent the use of insecure patterns in the codebase.

- **Scope**: Analyze all files in `src/tools/`.
- **Checks**:
  - Scan for raw `os.system` calls.
  - Scan for unsanitized `subprocess` calls.
- **Implementation**:
  - Use a static analysis tool or a custom script to identify these patterns.
  - Fail the pipeline if any occurrences are found.
- **Rationale**: Prevents "Security Negligence" by enforcing safe coding practices in forensic tools.

### 2. Typing Validation (Mypy/Pyright)
**Objective**: Enforce strict type-checking to ensure "Pydantic Rigor."

- **Scope**: Validate all Python files in the `src/` directory.
- **Checks**:
  - Ensure no `Any` types are used.
  - Verify that all functions have complete type hints.
  - Validate Pydantic models for field constraints and descriptions.
- **Implementation**:
  - Run `mypy` or `pyright` as part of the pipeline.
  - Fail the pipeline if any type errors are detected.
- **Rationale**: Ensures type safety and adherence to the project's strict typing standards.

### 3. The "Judicial Integrity" Test
**Objective**: Validate the robustness of the audit process through adversarial testing.

- **Scope**: Run a mock audit on a "broken" repository.
- **Checks**:
  - Ensure the Prosecutor detects intentional flaws in the mock repository.
  - Fail the pipeline if the flaws are not caught.
- **Implementation**:
  - Use a predefined "broken" repository as a test case.
  - Automate the audit process and verify the results.
- **Rationale**: Ensures the reliability and accuracy of the audit process.

### 4. The "Graph Architecture" Linter
**Objective**: Verify the correctness of the graph architecture.

- **Scope**: Analyze `src/graph.py`.
- **Checks**:
  - Ensure the file contains the necessary fan-out/fan-in wiring for Detectives and Judges.
  - Validate the structure against the Protocol requirements.
- **Implementation**:
  - Use a custom linter or static analysis tool to verify the architecture.
  - Fail the pipeline if the structure is incorrect.
- **Rationale**: Ensures the graph architecture adheres to the challenge specifications.

---

## Beyond the Rubric (Elite Tier)

### 5. LangSmith Integration Check
**Objective**: Ensure observability of all audits through LangChain tracing.

- **Scope**: Validate the presence of environment variables for LangChain tracing.
- **Checks**:
  - Verify that the required environment variables are set.
  - Fail the pipeline if any variables are missing.
- **Implementation**:
  - Use a script to check for the presence of the variables.
  - Log a warning if the variables are not set.
- **Rationale**: Ensures that every audit is observable and traceable.

### 6. Git Narrative Check
**Objective**: Enforce the "Forensic Progression" in commit messages.

- **Scope**: Analyze commit messages in the current branch.
- **Checks**:
  - Ensure commit messages follow the pattern: `Analysis -> Scaffolding -> Logic`.
  - Fail the pipeline if the pattern is not followed.
- **Implementation**:
  - Use a Git hook or a custom script to validate commit messages.
  - Provide feedback on non-compliant messages.
- **Rationale**: Maintains a clear and logical progression in the project's Git history.

---

By implementing this CI pipeline, the "Automaton Auditor" project will maintain the highest standards of security, reliability, and observability. Each stage is designed to enforce critical aspects of the challenge requirements and ensure the project's success.