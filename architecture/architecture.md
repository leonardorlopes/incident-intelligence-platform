# System Architecture - Incident Intelligence Platform

## 1. High-Level Architecture
The platform follows a microservices-based architecture integrated with an Agentic AI Orchestration layer.

### 1.1 Key Components
- **API Gateway:** Entry point for webhooks (ServiceNow, PagerDuty) and UI requests.
- **Orchestration Layer (LangGraph):** Manages the state and flow between specialized AI agents.
- **Agent Pool:** Collection of specialized agents (Analysis, Retrieval, RCA, etc.).
- **Vector Database:** Stores embedded technical documentation and historical incident data.
- **Relational Database:** Stores incident metadata, agent execution logs, and user configurations.
- **Knowledge Ingestion Pipeline:** ETL process that converts documentation (Markdown, PDF) into embeddings.

## 2. Agent Orchestration (LangGraph Flow)
The incident resolution process is modeled as a directed acyclic graph (DAG) or cyclic graph depending on the complexity:
1. **Ingestion Node:** Receives incident data.
2. **Analysis Agent:** Identifies incident type and extracts entities.
3. **Retrieval Agent:** Fetches relevant runbooks and documentation using RAG.
4. **Similar Incident Agent:** Queries the Vector DB for historical incidents with similar embeddings.
5. **Recommendation Agent:** Synthesizes findings into actionable steps.
6. **RCA Agent:** (Post-resolution) Generates the final RCA report.

## 3. RAG Flow & Context Engineering
Context is king in incident resolution. Our RAG implementation includes:
- **Hybrid Search:** Combining semantic search (embeddings) with keyword search (BM25) for high precision.
- **Context Injection:** Dynamically building prompts with the most relevant documentation snippets.
- **Context Window Management:** Pruning irrelevant information to keep LLM tokens focused on high-signal data.

## 4. Knowledge Ingestion Pipeline
- **Sources:** GitHub repos (Markdown), AWS Documentation, Internal Wiki.
- **Processing:** Chunking using semantic headers -> Embedding via OpenAI `text-embedding-3-small` -> Storage in Pinecone.

## 5. Integrations
- **ServiceNow:** Bi-directional sync. Updates incident work notes with agent findings.
- **AWS Deployment:**
  - Backend: AWS Fargate (ECS).
  - Database: Amazon RDS (PostgreSQL).
  - Vector DB: Pinecone (SaaS) or Weaviate on EKS.
  - CI/CD: GitHub Actions.

## 6. Security & Data Privacy
- **PII Redaction Service:** Middleware that scans incident text for sensitive data before LLM processing.
- **Audit Logging:** Every agent action and LLM call is logged for accountability.
