import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_separator():
    print("\n" + "="*60)

def test_incident(name, description, metadata=None):
    print_separator()
    print(f"TESTING SCENARIO: {name}")
    print(f"Description: {description}")
    print("-" * 60)
    
    payload = {
        "description": description,
        "metadata": metadata or {}
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/analyze", json=payload)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            analysis = result["analysis"]
            
            print(f"Status: {result['status']} (took {duration:.2f}s)")
            print(f"\nROOT CAUSE HYPOTHESIS:")
            print(f"-> {analysis['root_cause_hypothesis']}")
            
            print(f"\nSUGGESTED ACTIONS:")
            for i, action in enumerate(analysis['suggested_actions'], 1):
                print(f"{i}. {action}")
            
            print(f"\nConfidence: {analysis['confidence']:.2f}")
            
            if analysis['referenced_runbooks']:
                print(f"Referenced Runbooks: {', '.join(analysis['referenced_runbooks'])}")
            else:
                print("Referenced Runbooks: None (Using general AI knowledge)")
                
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to the server. Make sure main.py is running on localhost:8000")

if __name__ == "__main__":
    print("Starting Incident Intelligence Platform Test Client...")
    
    # Scenario 1: Kafka Lag (Should trigger RAG with kafka-consumer-lag.md)
    test_incident(
        "Kafka Consumer Lag",
        "We are seeing a massive spike in consumer lag for the 'orders-topic' in the production cluster. Processing is falling behind by 100k messages.",
        {"service": "orders-api", "environment": "production"}
    )
    
    # Scenario 2: Database Issues (Should trigger RAG with database-lock-contention.md)
    test_incident(
        "Database Performance",
        "The checkout database is reporting high CPU and many queries are stuck in 'Lock' status.",
        {"service": "checkout-db", "severity": "P1"}
    )
    
    # Scenario 3: Generic Application Error (No specific runbook, general AI analysis)
    test_incident(
        "Generic UI Error",
        "Users in the US-East region are reporting that the dashboard is showing a 'Data Load Error' with 500 status codes.",
        {"region": "us-east-1"}
    )
    
    print_separator()
    print("Testing Complete.")
