# Runbook: ECS Service Down

## Symptom
ECS Service tasks are failing health checks or failing to start, leading to service unavailability (HTTP 503/504).

## Diagnostic Steps
1. **Check Service Events:**
   - Look for "service [name] is unable to place a task because no container instance met all of its requirements".
2. **Inspect Stopped Task Reasons:**
   - Check the `StoppedReason` in the ECS console or via CLI: `aws ecs describe-tasks --tasks <task_id>`.
3. **Analyze CloudWatch Logs:**
   - Review application startup logs for crashes or missing environment variables.
4. **Verify Health Checks:**
   - Check Target Group health status and ALB logs.

## Common Causes
- **Memory/CPU Limits:** Task killed due to OOM (Out of Memory) or insufficient CPU.
- **Connectivity Issues:** Security groups or NACLs blocking traffic to the container.
- **Application Crash:** Code bug during initialization.
- **Missing Secrets:** Task failed to pull secrets from AWS Secrets Manager.

## Remediation Actions
- **Rollback:** Revert to the previous stable task definition version.
- **Scale Resources:** Increase memory/CPU limits in the task definition if OOM is detected.
- **Check IAM:** Ensure the task execution role has necessary permissions (e.g., ECR pull, Secret access).
- **Manual Restart:** Force a new deployment to trigger task replacement.

## Escalation
If the service remains unstable, escalate to the Cloud Infrastructure team.
