# Microservices Observability Strategy

## 1. The Three Pillars
- **Metrics:** Numerical data over time (CPU, latency, error rates). Use Prometheus/Grafana.
- **Logs:** Discrete events (Exceptions, audit trails). Use ELK Stack or Splunk.
- **Traces:** Path of a request through the system. Use OpenTelemetry and Jaeger/Honeycomb.

## 2. Distributed Tracing
Crucial for identifying which service in a chain is causing latency.
- **Trace ID:** Uniquely identifies a request flow.
- **Span ID:** Identifies a specific unit of work within a service.

## 3. Log Aggregation & Correlation
Ensure logs contain `trace_id` and `span_id`. This allows you to jump from a slow trace directly to the relevant logs in every service involved.

## 4. SLIs and SLOs
- **SLI (Indicator):** Error Rate of the Checkout Service.
- **SLO (Objective):** Error Rate < 0.1% over a rolling 30-day window.

## 5. Health Checks
- **Liveness:** Is the process running?
- **Readiness:** Is the service ready to accept traffic (e.g., is the DB connection established)?
- **Startup:** Used for slow-starting legacy applications.
