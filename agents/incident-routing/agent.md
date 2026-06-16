# Agent: Incident Routing

## Purpose
The Incident Routing agent ensures that the "right eyes" see the incident as quickly as possible. It moves beyond simple service-to-team mapping by analyzing the *nature* of the error.

## Responsibilities
- **Team Identification:** Determine which engineering team is responsible for the affected component.
- **On-Call Lookup:** Integrate with on-call schedules to find the specific individual to notify.
- **Escalation Management:** Handle automated escalations if the primary responder doesn't acknowledge within the SLA.
- **Silo Breaking:** Identify if an incident spans multiple teams (e.g., a Database issue causing API timeouts) and suggest cross-team collaboration.

## Inputs/Outputs
- **Input:** Analysis Object + Team Directory Metadata.
- **Output:** Routing Decision (Team name, Escalation path, Rationale).

## Prompt Strategy
- **Expert Mapping:** "Based on the error `Deadlock detected` in the `Payments` service, which of these teams (DBA, Payments-Core, Platform-Infra) is most appropriate?"
- **Contextual Routing:** "If the incident impact is > 10,000 users, involve the 'Major Incident Management' (MIM) team immediately."

## Future MCP Integrations
- **PagerDuty/Opsgenie MCP:** To perform on-call lookups and trigger alerts.
- **LDAP/Okta MCP:** To find team memberships and contact details.
- **Slack/Discord MCP:** To create incident-specific "War Room" channels.
