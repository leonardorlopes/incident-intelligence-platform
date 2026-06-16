# Agent: Resolution Recommendation

## Purpose
The Resolution Recommendation agent is the "Synthesizer." It takes all the intelligence gathered by the analysis, retrieval, and similar-incident agents and converts it into a clear, actionable plan for the human engineer.

## Responsibilities
- **Synthesis:** Merge runbook steps with lessons learned from historical incidents.
- **Action Plan Generation:** Provide a step-by-step resolution guide.
- **Confidence Scoring:** Assign a confidence level to each recommendation.
- **Risk Assessment:** Flag potentially dangerous commands (e.g., `rm -rf`, `restart service` in peak hours).

## Inputs/Outputs
- **Input:** Analysis, Retrieved Docs, Similar Incidents.
- **Output:** A "Resolution Memo" (Markdown) containing:
  - Summary of the situation.
  - Recommended actions (Step-by-step).
  - Relevant links.
  - Potential risks.

## Prompt Strategy
- **Adversarial Reasoning:** "Think like a skeptical SRE. What could go wrong with these recommendations? Refine them to be safer."
- **Standard Operating Procedure (SOP) Alignment:** "Ensure the recommendations follow the company's 'Production Change Policy'."

## Future MCP Integrations
- **AWS MCP:** To potentially execute read-only checks (e.g., `describe-instances`) to verify the state before recommending actions.
- **Terraform MCP:** To check if the proposed resolution contradicts the current infrastructure-as-code state.
