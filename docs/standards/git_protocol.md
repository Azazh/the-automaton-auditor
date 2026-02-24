# Git Protocol Standard

## Forensic Git Progression
To ensure traceability and maintain a clean history, follow these guidelines:

### Commit Standards
- Use **Conventional Commits** for all commit messages. Examples:
  - `feat: Add AST parsing for graph validation`
  - `fix: Handle missing files in PDF parser`
  - `chore: Update documentation for testing SOP`

### Commit Sequence
1. **Scaffolding:** Initial setup of directories and files.
2. **Forensic Tooling:** Implementation of Detective tools (e.g., AST analyzer, Git forensics).
3. **Judicial Logic:** Development of Judge personas and their decision-making logic.
4. **Integration:** Connecting Detectives, Judges, and the Chief Justice into a cohesive StateGraph.
5. **Adversarial Testing:** Adding test cases to validate the robustness of the system.

### Atomic Commits
- Each commit should represent a single, logical change. Avoid bundling unrelated changes into one commit.
- Write clear, descriptive commit messages to explain the purpose of the change.