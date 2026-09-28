from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from src.orchestration.orchestrator import NewsOrchestrator
from src.rag.query_engine import RAGQueryEngine

app = FastAPI(
    title="AI News Analyst API",
    description="REST API for multi-agent news ingestion and grounded RAG query engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = NewsOrchestrator()
query_engine = RAGQueryEngine(vector_store=orchestrator.vector_store)

# Run initial ingestion
orchestrator.run_pipeline("all")

class QueryRequest(BaseModel):
    question: str
    category: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

@app.get("/")
def root():
    return {"status": "online", "message": "AI News Analyst RAG API Server"}

@app.post("/api/v1/rag/query")
def query_rag(request: QueryRequest):
    try:
        res = query_engine.query(
            question=request.question,
            override_category=request.category,
            override_start_date=request.start_date
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/briefing")
def get_briefing():
    return query_engine.generate_daily_briefing()

@app.post("/api/v1/orchestration/trigger")
def trigger_ingestion(category: str = "all"):
    res = orchestrator.run_pipeline(category)
    return res
