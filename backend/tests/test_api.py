import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys
import os

# Adiciona o diretório pai (backend) ao sys.path para evitar ModuleNotFoundError
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)

# Mock response structure that mimics Gemini's response object
class MockGeminiResponse:
    def __init__(self, text):
        self.text = text

@pytest.fixture
def mock_gemini():
    with patch("google.generativeai.GenerativeModel.generate_content") as mock:
        yield mock

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "AI-Powered" in response.json()["platform"]

def test_analyze_with_mock_ai(mock_gemini):
    # Configurando o Mock para retornar um JSON válido de análise
    mock_json_response = {
        "root_cause_hypothesis": "Mocked Root Cause: Database overload",
        "suggested_actions": ["Scale DB", "Check slow queries"],
        "confidence": 0.95
    }
    mock_gemini.return_value = MockGeminiResponse(text=import_json_string(mock_json_response))

    payload = {
        "description": "The database is very slow today",
        "metadata": {"env": "prod"}
    }
    
    # Precisamos garantir que a API Key pareça estar configurada para o teste não dar fallback
    with patch("os.getenv", return_value="fake_key"):
        response = client.post("/analyze", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["analysis"]["root_cause_hypothesis"] == "Mocked Root Cause: Database overload"
    assert data["analysis"]["confidence"] == 0.95

def test_rag_integration_with_mock(mock_gemini):
    # Testando se o RAG encontra o runbook de Kafka e a IA recebe isso
    mock_json_response = {
        "root_cause_hypothesis": "Kafka lag identified from runbook",
        "suggested_actions": ["Follow kafka-consumer-lag.md steps"],
        "confidence": 0.9
    }
    mock_gemini.return_value = MockGeminiResponse(text=import_json_string(mock_json_response))

    payload = {
        "description": "High kafka lag in partition 5",
    }
    
    with patch("os.getenv", return_value="fake_key"):
        response = client.post("/analyze", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    # Verifica se o serviço de RAG anexou o runbook correto
    assert "kafka-consumer-lag.md" in data["analysis"]["referenced_runbooks"]

def import_json_string(dict_data):
    import json
    return json.dumps(dict_data)
