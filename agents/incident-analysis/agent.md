# Agent: Incident Analysis

## Purpose
The Incident Analysis agent is the first point of contact for any incoming incident. Its primary role is to "make sense" of the raw incident data, which is often messy and unstructured.

## Responsibilities
- **Categorization:** Classify the incident into predefined categories (e.g., Network, Database, Application, Infrastructure).
- **Prioritization Validation:** Verify if the incoming priority (P1-P4) matches the description.
- **Entity Extraction:** Extract critical entities like Service Name, Hostname, Error Codes, Affected Regions, and User Impact.
- **Sentiment Analysis:** Detect the urgency and tone of the incident reporter.

## Inputs/Outputs
- **Input:** Raw JSON from ServiceNow/PagerDuty (Description, Short Description, Metadata).
- **Output:** Structured Analysis Object (JSON) containing categories, entities, and an "Analysis Summary."

## Prompt Strategy
- **Few-Shot Prompting:** Provide examples of raw incident logs and their corresponding structured outputs.
- **Role-Based:** "You are a Senior SRE specialized in rapid incident triage. Analyze the following incident report..."
- **Chain-of-Thought:** Instruct the model to first list its observations before finalizing the extraction.

## Future MCP Integrations
- **ServiceNow MCP:** To update incident records directly.
- **Jira MCP:** To search for related bug reports.
- **Slack MCP:** To notify relevant channels during high-priority analysis.
