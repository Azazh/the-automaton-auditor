# Interim Report Draft

## Architecture Decisions
- **StateGraph Orchestration**: The graph was designed with a fan-out to parallel detectives (`RepoInvestigator` and `DocAnalyst`) and a fan-in to the `EvidenceAggregator`.
- **Conditional Edge**: An `ErrorNode` was added to handle invalid inputs gracefully.

## AST vs Regex Trade-offs
- **AST**: Provides structural validation and ensures correctness in graph wiring.
- **Regex**: Faster but prone to false positives and lacks structural guarantees.
- **Decision**: AST was chosen for its rigor and alignment with the "Protocol B: Graph Wiring" requirement.

## Planned Judicial Logic
- **JudicialBench**: Will be implemented in the final submission to evaluate evidence and issue rulings.
- **Scoring**: Each piece of evidence will be scored based on confidence and rationale.