import os
import uuid
import json
import glob
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    model = genai.GenerativeModel(model_name)
else:
    model = None

app = FastAPI(
    title="Incident Intelligence Platform API",
    description="Multi-agent orchestration for autonomous incident resolution.",
    version="1.1.0"
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

# --- RAG Utility (Knowledge Retrieval) ---

class KnowledgeService:
    @staticmethod
    def get_context_from_runbooks(query: str) -> str:
        """Simple RAG implementation: find runbooks that match keywords in the query."""
        runbook_dir = os.path.join(os.path.dirname(__file__), "../../runbooks/*.md")
        runbooks = glob.glob(runbook_dir)
        
        context_parts = []
        referenced = []
        
        # In a production RAG, we would use vector embeddings. 
        # Here we use a keyword-based retrieval for simplicity and speed.
        query_words = set(query.lower().split())
        
        for rb_path in runbooks:
            filename = os.path.basename(rb_path)
            # Check if filename keywords are in the query
            name_keywords = set(filename.replace(".md", "").replace("-", " ").lower().split())
            
            if query_words.intersection(name_keywords):
                with open(rb_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    context_parts.append(f"--- Runbook: {filename} ---\n{content}")
                    referenced.append(filename)
        
        return "\n\n".join(context_parts), referenced

# --- AI Service Layer ---

class IncidentAnalysisService:
    @staticmethod
    async def analyze(request: IncidentRequest) -> AnalysisSuggestion:
        if not model:
            # Fallback for when API Key is missing
            return AnalysisSuggestion(
                root_cause_hypothesis="Gemini API Key not configured. Analysis is unavailable.",
                suggested_actions=["Configure GEMINI_API_KEY in .env file"],
                confidence=0.0,
                referenced_runbooks=[]
            )

        # 1. Retrieve Context (RAG)
        context, referenced = KnowledgeService.get_context_from_runbooks(request.description)
        
        # 2. Construct Prompt
        prompt = f"""
        You are an expert Site Reliability Engineer (SRE).
        Analyze the following incident and provide a structured response in JSON format.
        
        Incident Description: {request.description}
        Metadata: {json.dumps(request.metadata)}
        
        Use the following internal runbooks as context if relevant:
        {context if context else "No specific runbooks found for this query."}
        
        Your response must be a valid JSON object with these keys:
        - root_cause_hypothesis: A clear, concise technical theory.
        - suggested_actions: A list of specific, actionable steps.
        - confidence: A number between 0 and 1 representing your certainty.
        
        Ensure the JSON is well-formatted.
        """

        try:
            # 3. Call Gemini
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json"
                )
            )
            
            # 4. Parse Response
            analysis_data = json.loads(response.text)
            
            return AnalysisSuggestion(
                root_cause_hypothesis=analysis_data.get("root_cause_hypothesis", "Unable to determine"),
                suggested_actions=analysis_data.get("suggested_actions", []),
                confidence=float(analysis_data.get("confidence", 0.5)),
                referenced_runbooks=referenced
            )
        except Exception as e:
            print(f"AI Analysis Error: {e}")
            raise HTTPException(status_code=500, detail="AI Analysis failed to process the request.")

# --- Endpoints ---

@app.get("/")
async def root():
    return {"status": "online", "platform": "Incident Intelligence (AI-Powered)"}

@app.post("/analyze", response_model=IncidentResponse)
async def analyze_incident(request: IncidentRequest):
    incident_id = request.id or str(uuid.uuid4())
    analysis = await IncidentAnalysisService.analyze(request)
    return IncidentResponse(
        incident_id=incident_id,
        status="analyzed",
        analysis=analysis
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
