# Runbook: High API Latency

## Symptom
P99 latency exceeding SLAs. Users reporting slow response times. Error rates may also increase.

## Diagnostic Steps
1. **Identify the Bottleneck:**
   - Use APM (Datadog/NewRelic) to trace requests. Is it the DB, an external API, or the application code?
2. **Check System Metrics:**
   - Check CPU/Memory of API servers. Is there high context switching or disk I/O?
3. **Analyze External Dependencies:**
   - Check if downstream services are also experiencing latency.

## Common Causes
- **Cold Starts:** (If using Lambda) Concurrent requests triggering new environment initialization.
- **Downstream Failure:** A dependent service is slow but not failing (no circuit breaker).
- **Resource Exhaustion:** Thread pool or connection pool saturation.
- **Inefficient Serialization:** Large JSON payloads being processed synchronously.

## Remediation Actions
- **Scale Out:** Increase the number of API instances.
- **Cache Responses:** Enable or clear Redis/CDN caches.
- **Circuit Breaking:** Manually trip circuit breakers if a downstream service is the bottleneck.
- **Traffic Shifting:** Redirect traffic to a healthy region or cluster if possible.

## Escalation
If latency is global across all services, escalate to the Network/Platform team.
