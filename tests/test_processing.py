import pytest
from src.agents.processing_agent import ProcessingAgent

def test_deduplication():
    agent = ProcessingAgent()
    sample_articles = [
        {
            "article_id": "a1",
            "headline": "RBI Keeps Rate Unchanged",
            "body": "The Reserve Bank of India kept repo rate at 6.5%",
            "source": "Source A"
        },
        {
            "article_id": "a2",
            "headline": "RBI Keeps Rate Unchanged",  # Duplicate headline
            "body": "The Reserve Bank of India kept repo rate at 6.5%",
            "source": "Source B"
        }
    ]
    deduped = agent.deduplicate(sample_articles)
    assert len(deduped) == 1
    assert deduped[0]["article_id"] == "a1"

def test_entity_extraction():
    agent = ProcessingAgent()
    text = "Narendra Modi and Governor Shaktikanta Das discussed RBI monetary policy in New Delhi with NVIDIA executives."
    entities = agent.extract_entities(text)
    assert "RBI" in entities or "NVIDIA" in entities
    assert "Modi" in entities or "Das" in entities or "New Delhi" in entities

def test_chunking():
    agent = ProcessingAgent(chunk_size=10, chunk_overlap=2)
    long_text = " ".join([f"word{i}" for i in range(25)])
    chunks = agent.chunk_text(long_text)
    assert len(chunks) > 1
