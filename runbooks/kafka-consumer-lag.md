# Runbook: Kafka Consumer Lag

## Symptom
Increasing lag in Kafka consumers, leading to delayed data processing and potential system inconsistency.

## Diagnostic Steps
1. **Check Consumer Group Status:**
   - Run: `kafka-consumer-groups --bootstrap-server <broker> --describe --group <group_name>`
2. **Analyze Partition Distribution:**
   - Check if the lag is concentrated in specific partitions or spread across all.
3. **Inspect Consumer Logs:**
   - Look for `CommitFailedException`, `RebalanceInProgress`, or long processing times per message.
4. **Monitor Resource Utilization:**
   - Check CPU/Memory of consumer instances in Datadog.

## Common Causes
- **Processing Bottleneck:** The time to process a single message is higher than the arrival rate.
- **Frequent Rebalancing:** Unstable consumer heartbeats or long processing times exceeding `max.poll.interval.ms`.
- **Uneven Data Distribution:** "Hot" partitions due to poor choice of partition keys.

## Remediation Actions
- **Scale Out:** Increase the number of consumer instances (up to the number of partitions).
- **Optimize Code:** Profile the consumer processing logic for bottlenecks.
- **Tuning:** Increase `max.poll.records` or adjust `fetch.min.bytes` to improve throughput.
- **Reset Offsets:** In extreme cases, skip non-critical lag using `--reset-offsets`.

## Escalation
If lag persists after scaling and tuning, escalate to the Data Platform team.
