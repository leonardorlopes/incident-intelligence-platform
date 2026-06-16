# Runbook: Database Lock Contention

## Symptom
High database CPU, long-running queries, and application timeouts. Monitoring shows an increase in "Wait Events" related to locks.

## Diagnostic Steps
1. **Identify Blocked Sessions:**
   - For PostgreSQL: `SELECT * FROM pg_stat_activity WHERE wait_event_type = 'Lock';`
2. **Check Long Running Transactions:**
   - `SELECT pid, now() - xact_start AS duration, query FROM pg_stat_activity WHERE state <> 'idle' ORDER BY duration DESC;`
3. **Analyze Deadlocks:**
   - Check PostgreSQL logs for "deadlock detected" messages.

## Common Causes
- **Missing Indexes:** Queries performing sequential scans holding locks longer.
- **Large Transactions:** Too many updates/deletes in a single transaction.
- **Unoptimized Queries:** SELECT FOR UPDATE used unnecessarily.

## Remediation Actions
- **Kill Blockers:** Terminate the backend PID of the blocking session: `SELECT pg_terminate_backend(<pid>);`
- **Optimize Transaction:** Break large updates into smaller batches.
- **Add Indexes:** Create missing indexes to speed up the identifying of rows.
- **Vacuum/Analyze:** Run `ANALYZE` to update statistics and improve the query planner.

## Escalation
If performance doesn't recover after killing blockers, escalate to the DBA team.
