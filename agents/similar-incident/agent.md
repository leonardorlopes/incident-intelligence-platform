# Agent: Similar Incident

## Purpose
The Similar Incident agent identifies historical "precedents." It looks for past incidents that share similar error patterns, affected components, or resolution paths to avoid reinventing the wheel.

## Responsibilities
- **Pattern Matching:** Use embeddings to find semantically similar incidents in the historical database.
- **Resolution Extraction:** Extract what was actually done to fix those similar incidents (from work notes).
- **Outcome Analysis:** Check if the previous resolutions were successful or if they led to regressions.

## Inputs/Outputs
- **Input:** Structured Analysis Object + Current Context.
- **Output:** Top 3-5 similar incidents with summaries of their causes and resolutions.

## Prompt Strategy
- **Comparative Analysis:** "Compare the current incident with the following historical incident. Are the root causes likely the same? Why or why not?"
- **Constraint-Based:** "Only consider incidents resolved in the last 6 months to ensure architectural relevance."

## Future MCP Integrations
- **Elasticsearch/Splunk MCP:** To query historical log patterns.
- **Dynatrace/Datadog MCP:** To compare metric spikes from the past with the current incident.
