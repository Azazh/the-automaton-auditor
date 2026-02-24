# Pragmatic Testing Standard Operating Procedure (SOP)

## Tool Validation
Every Detective tool in `src/tools/` must have a unit test ensuring it returns "No Evidence Found" instead of crashing when a file is missing. This ensures robustness and graceful failure handling.

## Persona Consistency
Define a "Golden Test Case"—a mock repository with known flaws. The test must verify:
- The Prosecutor identifies the flaw and assigns a low score.
- The Defense attempts to justify the flaw and assigns a higher score.
- The Tech Lead provides a balanced, pragmatic assessment.

## Deterministic Output
All judges must return structured JSON outputs. This ensures that the "Chief Justice" can parse results deterministically without relying on regex or freeform text parsing. Structured outputs improve reliability and reduce ambiguity in the decision-making process.