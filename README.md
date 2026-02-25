# Automaton Auditor

## Overview
The Automaton Auditor is a LangGraph-based system designed to audit workflows with forensic accuracy and judicial rigor. This interim submission focuses on the Detective Layer and StateGraph orchestration.

## Architecture

### Diagram
```
Parallel Detectives -> Evidence Aggregator -> END
```
- **Parallel Detectives**: The `RepoInvestigator` and `DocAnalyst` nodes run concurrently to collect evidence.
- **Evidence Aggregator**: Aggregates and validates evidence from the detectives.
- **END**: Placeholder for the JudicialBench (to be implemented in the final submission).

## Installation

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Fill in REPO_URL and PDF_PATH
   ```

## Running the Audit

1. Execute the interim audit:
   ```bash
   python src/main.py
   ```

2. Ensure `LANGCHAIN_TRACING_V2` is set to `true` for observability (optional).