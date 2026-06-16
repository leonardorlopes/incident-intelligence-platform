# Amazon ECS Performance Optimization Guide

## 1. Task Sizing
Ensuring your tasks have the right amount of CPU and Memory is critical for stability and cost.
- **Over-provisioning:** Leads to wasted costs.
- **Under-provisioning:** Leads to OOM (Out of Memory) kills and CPU throttling.

**Recommendation:** Use AWS Compute Optimizer to analyze historical task metrics and suggest optimal sizes.

## 2. Fargate vs. EC2
- **Fargate:** Best for "set and forget" management.
- **EC2:** Best for high-performance workloads requiring custom AMI or specific instance types (e.g., GPU).

## 3. Storage Optimization
Avoid using task storage for persistent data. Use Amazon EFS for shared, persistent storage across ECS tasks.

## 4. Troubleshooting "Task Stopped"
- **Reason: Essential container in task exited.**
  - *Resolution:* Check CloudWatch Logs for application-level crashes.
- **Reason: Out of Memory (OOM).**
  - *Resolution:* Increase memory limit in task definition or optimize application heap usage.

## 5. Networking
Prefer `awsvpc` network mode for better security and performance, as each task gets its own Elastic Network Interface (ENI).
