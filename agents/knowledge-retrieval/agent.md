# Agent: Knowledge Retrieval

## Purpose
The Knowledge Retrieval agent acts as the platform's librarian, searching through vast amounts of technical documentation and runbooks to find the most relevant context for the current incident.

## Responsibilities
- **Context Search:** Perform semantic searches against the Vector Database using incident entities as queries.
- **Filtering:** Filter out outdated or irrelevant documentation.
- **Context Synthesis:** Chunk and format retrieved snippets to be consumed by other agents.
- **Missing Knowledge Identification:** Flag incidents where no relevant documentation is found, signaling a gap in the runbook repository.

## Inputs/Outputs
- **Input:** Structured Analysis Object (from Incident Analysis Agent).
- **Output:** A list of "Context Snippets" (Markdown) with source links and relevance scores.

## Prompt Strategy
- **Re-ranking:** Use the LLM to re-rank search results from the Vector DB based on their exact relevance to the incident's technical stack.
- **Instructional:** "Given the following service and error, retrieve and summarize the most relevant troubleshooting steps from our internal runbooks."

## Future MCP Integrations
- **GitHub MCP:** To fetch the latest documentation from the `docs/` folder in service repositories.
- **Confluence MCP:** To search internal enterprise wikis.
- **Stack Overflow Enterprise MCP:** To find internal developer discussions.
