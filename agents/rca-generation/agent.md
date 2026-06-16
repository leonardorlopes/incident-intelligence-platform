# Agent: RCA Generation

## Purpose
The RCA (Root Cause Analysis) Generation agent automates the most time-consuming part of the incident lifecycle: the post-mortem report. It runs after the incident is marked as 'Resolved'.

## Responsibilities
- **Timeline Construction:** Build a chronological timeline of events (Detection, Triage, Investigation, Resolution).
- **Root Cause Identification:** Analyze the chain of events to identify the "Primary" and "Contributing" causes.
- **Action Item Proposal:** Suggest long-term fixes to prevent recurrence.
- **Tone Adjustment:** Ensure the report is "Blameless" and focused on systemic improvements.

## Inputs/Outputs
- **Input:** Full incident log, agent work notes, resolution details.
- **Output:** A draft RCA Document (Markdown/PDF).

## Prompt Strategy
- **The "5 Whys" Technique:** Instruct the agent to apply the "5 Whys" methodology to reach the root cause.
- **Template-Driven:** "Populate the standard corporate RCA template using the following incident history..."

## Future MCP Integrations
- **GitHub MCP:** To identify which specific PR or commit introduced the bug.
- **Confluence MCP:** To publish the final RCA directly to the Post-Mortem space.
- **Statuspage MCP:** To generate a public-facing summary of the incident.
