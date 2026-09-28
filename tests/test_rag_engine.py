import pytest
import tempfile
import shutil
from src.knowledge_base.vector_store import NewsVectorStore
from src.rag.query_engine import RAGQueryEngine
from src.rag.reranker import RecencyReranker

def test_intent_parser():
    engine = RAGQueryEngine(vector_store=None)
    intent1 = engine.parse_query_intent("What did the RBI announce this week and how did markets react?")
    assert intent1["category"] == "Finance"
    assert intent1["start_date"] is not None

    intent2 = engine.parse_query_intent("NVIDIA released new AI GPU architecture")
    assert intent2["category"] == "Tech"

def test_recency_reranker():
    reranker = RecencyReranker()
    sample_results = [
        {
            "content": "RBI announcement from 10 days ago",
            "similarity": 0.9,
            "metadata": {"published_date": "2026-09-17"}
        },
        {
            "content": "RBI announcement from yesterday",
            "similarity": 0.85,
            "metadata": {"published_date": "2026-09-27"}
        }
    ]
    reranked = reranker.rerank("RBI announcement", sample_results, top_k=2)
    assert len(reranked) == 2
    assert "composite_score" in reranked[0]

def test_unanswerable_fallback():
    temp_dir = tempfile.mkdtemp()
    store = NewsVectorStore(persist_dir=temp_dir, collection_name="test_empty")
    engine = RAGQueryEngine(vector_store=store)
    
    res = engine.query("What is the secret recipe for Martian space pie?")
    assert res["found_matches"] is False
    assert "I don't have news on that" in res["answer"]
    
    shutil.rmtree(temp_dir, ignore_errors=True)
