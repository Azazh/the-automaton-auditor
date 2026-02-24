# Guidelines for justice.py

# 1. Implement deterministic Python logic for conflict resolution.
# 2. Define hardcoded rules for:
#    - Security Override: Security flaws cap scores at 3.
#    - Fact Supremacy: Forensic evidence overrides subjective opinions.
#    - Dissent Requirement: Summarize disagreements among judges when score variance > 2.
# 3. Ensure the ChiefJusticeNode synthesizes judge opinions into a final verdict.
# 4. Output the final AuditReport as structured Markdown for transparency.
# 5. Handle edge cases where evidence is missing or contradictory.