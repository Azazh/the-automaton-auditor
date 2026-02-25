# ⚖️ The Automaton Auditor: Autonomous Governance Swarm

> **Mission Statement**: The Automaton Auditor shifts the paradigm from code generation to code governance, ensuring forensic accuracy, judicial rigor, and autonomous compliance in software workflows.

---

## 🏛️ Architecture: The Digital Courtroom

The Automaton Auditor employs a **Hierarchical State Graph** modeled as a "Digital Courtroom":

- **Forensic Layer (Detectives)**: Parallel nodes (`RepoInvestigator`, `DocAnalyst`) gather structured evidence.
- **Judicial Layer (Judges)**: Evaluates evidence with dialectic scoring and persona integrity.
- **Synthesis Layer (Supreme Court)**: Resolves conflicts deterministically, ensuring governance compliance.

---

## 🛠️ Core Tech Stack

| Technology   | Purpose                                      |
|--------------|---------------------------------------------|
| **LangGraph**| Orchestrates parallel workflows             |
| **Pydantic** | Enforces state rigor and validation         |
| **AST**      | Enables structural forensic analysis        |

---

## 🚀 Interim Features

### Parallel Detectives
- **RepoInvestigator**: Analyzes repository structure and git history.
- **DocAnalyst**: Extracts and validates evidence from PDF documents.

### Forensic Tools
- **Sandboxed Git Cloning**: Ensures secure repository interactions.
- **AST-Based Graph Verification**: Validates structural integrity of workflows.

---

## ⚙️ Setup & Usage

### Installation

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Fill in REPO_URL and PDF_PATH
   ```

### Running the Audit

1. Execute the audit against a target repository:
   ```bash
   python src/main.py --url <repo_url>
   ```

2. (Optional) Enable observability:
   ```bash
   export LANGCHAIN_TRACING_V2=true
   ```

---

## 📜 Project Governance

> **Commit Standards**: This project adheres to [Conventional Commits](https://www.conventionalcommits.org/).

> **Forensic Git History**: Every commit is traceable, ensuring accountability and transparency.

---