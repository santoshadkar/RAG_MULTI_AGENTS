import pytest
import shutil
import tempfile
from src.knowledge_base.vector_store import NewsVectorStore

@pytest.fixture
def temp_vector_store():
    temp_dir = tempfile.mkdtemp()
    store = NewsVectorStore(persist_dir=temp_dir, collection_name="test_collection")
    yield store
    shutil.rmtree(temp_dir, ignore_errors=True)

def test_add_and_search_chunks(temp_vector_store):
    sample_chunks = [
        {
            "chunk_id": "test_chunk_01",
            "article_id": "art_01",
            "headline": "RBI Announces Policy Rate Stability",
            "content": "The Reserve Bank of India maintained repo rate at 6.5%.",
            "summary": "RBI rate unchanged.",
            "entities": "RBI, Repo Rate",
            "source": "Economic Times",
            "url": "https://example.com/rbi",
            "published_date": "2026-09-27",
            "category": "Finance"
        }
    ]
    temp_vector_store.add_chunks(sample_chunks)
    assert temp_vector_store.get_stats()["total_chunks"] == 1

    results = temp_vector_store.search("What did RBI announce?", top_k=5, category="Finance")
    assert len(results) == 1
    assert results[0]["metadata"]["headline"] == "RBI Announces Policy Rate Stability"
