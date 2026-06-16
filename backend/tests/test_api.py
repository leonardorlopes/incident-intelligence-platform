import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_analyze_kafka_lag():
    payload = {
        "id": "test-inc-001",
        "description": "High Kafka consumer lag detected on production cluster",
        "metadata": {"service": "order-processor", "env": "prod"}
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["incident_id"] == "test-inc-001"
    assert "Kafka" in data["analysis"]["root_cause_hypothesis"]
    assert "kafka-consumer-lag.md" in data["analysis"]["referenced_runbooks"]

def test_analyze_latency():
    payload = {
        "description": "Slow API responses and timeouts observed in the checkout service",
        "metadata": {"tags": ["checkout", "p99"]}
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "latency" in data["analysis"]["root_cause_hypothesis"].lower()
    assert len(data["analysis"]["suggested_actions"]) > 0

def test_analyze_ecs_down():
    payload = {
        "description": "ECS Service is reporting 503 errors and tasks are restarting",
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "ECS" in data["analysis"]["root_cause_hypothesis"]
    assert "ecs-service-down.md" in data["analysis"]["referenced_runbooks"]

def test_unknown_incident():
    payload = {
        "description": "Something strange is happening with the printer",
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["analysis"]["confidence"] == 0.5
    assert "Unknown" in data["analysis"]["root_cause_hypothesis"]
