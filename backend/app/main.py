from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import uuid

app = FastAPI(
    title="Incident Intelligence Platform API",
    description="Multi-agent orchestration for autonomous incident resolution.",
    version="1.0.0"
)

# --- Models ---

class IncidentRequest(BaseModel):
    id: Optional[str] = Field(None, description="Optional external ID for the incident")
    description: str = Field(..., description="Full description of the issue")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Contextual data (tags, service, region, etc.)")
    payload: Optional[Dict[str, Any]] = Field(None, description="Raw event data or log snippet")

class AnalysisSuggestion(BaseModel):
    root_cause_hypothesis: str
    suggested_actions: List[str]
    confidence: float
    referenced_runbooks: List[str]

class IncidentResponse(BaseModel):
    incident_id: str
    status: str
    analysis: AnalysisSuggestion

# --- Service Layer (Simulated Agent Logic) ---

class IncidentAnalysisService:
    @staticmethod
    async def analyze(request: IncidentRequest) -> AnalysisSuggestion:
        desc = request.description.lower()
        
        # Simple heuristic-based "intelligence" to simulate RAG/Agent behavior
        # In a real scenario, this would trigger the LangGraph agents
        if "lag" in desc or "kafka" in desc:
            return AnalysisSuggestion(
                root_cause_hypothesis="Potential Kafka partition imbalance or consumer bottleneck.",
                suggested_actions=[
                    "Check consumer group lag metrics.",
                    "Verify partition key distribution.",
                    "Scale out consumer instances if CPU is high."
                ],
                confidence=0.92,
                referenced_runbooks=["kafka-consumer-lag.md"]
            )
        elif "latency" in desc or "slow" in desc:
            return AnalysisSuggestion(
                root_cause_hypothesis="High P99 latency detected in downstream services or database contention.",
                suggested_actions=[
                    "Analyze database lock wait times.",
                    "Verify circuit breaker status for downstream dependencies.",
                    "Check for resource saturation on the API nodes."
                ],
                confidence=0.85,
                referenced_runbooks=["high-api-latency.md", "database-lock-contention.md"]
            )
        elif "down" in desc or "503" in desc or "ecs" in desc:
            return AnalysisSuggestion(
                root_cause_hypothesis="ECS Service unavailability due to task failure or failing health checks.",
                suggested_actions=[
                    "Check ECS task stopped reason.",
                    "Review application startup logs in CloudWatch.",
                    "Verify security group and ALB configuration."
                ],
                confidence=0.88,
                referenced_runbooks=["ecs-service-down.md"]
            )
        else:
            return AnalysisSuggestion(
                root_cause_hypothesis="Unknown incident pattern. Manual triage recommended.",
                suggested_actions=["Collect more logs", "Escalate to on-call engineer"],
                confidence=0.5,
                referenced_runbooks=[]
            )

# --- Endpoints ---

@app.get("/")
async def root():
    return {"status": "online", "platform": "Incident Intelligence"}

@app.post("/analyze", response_model=IncidentResponse)
async def analyze_incident(request: IncidentRequest):
    incident_id = request.id or str(uuid.uuid4())
    
    try:
        analysis = await IncidentAnalysisService.analyze(request)
        return IncidentResponse(
            incident_id=incident_id,
            status="analyzed",
            analysis=analysis
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
