# Testing the Incident Intelligence Platform

This project uses `pytest` for integration testing of the backend API.

## Prerequisites

Ensure you have the dependencies installed:

```bash
cd backend
pip install -r requirements.txt
pip install pytest httpx
```

## Running Tests

To run the integration tests, navigate to the `backend` directory and execute:

```bash
$env:PYTHONPATH = "." # For PowerShell
# OR
export PYTHONPATH=. # For Bash/Linux/macOS

pytest tests/test_api.py
```

## Test Coverage

The current tests cover:
- **Root Endpoint:** Basic health check.
- **Kafka Lag Analysis:** Verifies pattern matching and runbook referencing for Kafka issues.
- **Latency Analysis:** Verifies detection of performance-related incidents.
- **ECS Service Down:** Verifies detection of infrastructure availability issues.
- **Unknown Incidents:** Verifies the fallback logic for unrecognized patterns.

## Adding New Tests

New tests should be added to the `backend/tests/` directory. Use the `TestClient` from `fastapi.testclient` to simulate requests to the application.
