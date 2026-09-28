import re
import datetime
from typing import List, Dict, Any, Optional
from src.knowledge_base.vector_store import NewsVectorStore
from src.rag.reranker import RecencyReranker
from src.rag.prompts import GROUNDED_RAG_SYSTEM_PROMPT
from src.utils.config import OPENAI_API_KEY, LLM_MODEL_NAME
from src.utils.logger import get_logger

logger = get_logger("QueryEngine")

class RAGQueryEngine:
    def __init__(self, vector_store: Optional[NewsVectorStore] = None):
        self.vector_store = vector_store or NewsVectorStore()
        self.reranker = RecencyReranker()

    def parse_query_intent(self, query: str) -> Dict[str, Any]:
        """Step 1: Infer target category and temporal date range from query string"""
        query_lower = query.lower()
        category = "all"
        
        if any(w in query_lower for w in ["rbi", "sebi", "market", "stock", "sensex", "nifty", "repo rate", "finance", "economy", "bank", "fed", "inflation"]):
            category = "Finance"
        elif any(w in query_lower for w in ["ai", "nvidia", "google", "deepmind", "openai", "tech", "chip", "software", "app", "hacker"]):
            category = "Tech"
        elif any(w in query_lower for w in ["cabinet", "pib", "election", "parliament", "bill", "politics", "minister", "government", "diplomacy"]):
            category = "Politics"

        # Time range inference
        today = datetime.date.today()
        start_date = None
        end_date = today.strftime("%Y-%m-%d")

        if "this week" in query_lower or "past week" in query_lower or "last 7 days" in query_lower:
            start_date = (today - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        elif "today" in query_lower:
            start_date = today.strftime("%Y-%m-%d")
        elif "yesterday" in query_lower:
            start_date = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

        return {
            "category": category,
            "start_date": start_date,
            "end_date": end_date
        }

    def generate_grounded_answer(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        """Step 4: Generate grounded answer using retrieved context"""
        if not chunks:
            return "I don't have news on that based on the current knowledge base."

        # If OpenAI API Key is provided, call OpenAI API
        if OPENAI_API_KEY:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=OPENAI_API_KEY)
                context_str = "\n\n".join([
                    f"--- Source: {c['metadata']['source']} ({c['metadata']['published_date']}) ---\n"
                    f"Headline: {c['metadata']['headline']}\n"
                    f"Content: {c['content']}\n"
                    f"URL: {c['metadata']['url']}"
                    for c in chunks
                ])
                
                messages = [
                    {"role": "system", "content": GROUNDED_RAG_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Context:\n{context_str}\n\nQuestion: {query}"}
                ]
                
                response = client.chat.completions.create(
                    model=LLM_MODEL_NAME,
                    messages=messages,
                    temperature=0.2
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                logger.error(f"OpenAI API call failed: {e}. Falling back to deterministic grounded synthesizer.")

        # Fallback Deterministic Grounded Synthesizer
        answer_parts = []
        for c in chunks:
            meta = c["metadata"]
            headline = meta.get("headline", "News Update")
            source = meta.get("source", "News Source")
            pub_date = meta.get("published_date", "Recent")
            url = meta.get("url", "#")
            summary = meta.get("summary") or c["content"][:250] + "..."
            
            answer_parts.append(
                f"• **{headline}** ({pub_date})\n"
                f"  {summary}\n"
                f"  *Source*: [{source}]({url})"
            )

        bullet_points = "\n\n".join(answer_parts)
        return f"Based on collected news updates, here is what was reported:\n\n{bullet_points}"

    def query(
        self,
        question: str,
        override_category: Optional[str] = None,
        override_start_date: Optional[str] = None,
        top_k: int = 5
    ) -> Dict[str, Any]:
        logger.info(f"Processing user question: '{question}'")
        
        # Step 1: Intent & Filter Interpretation
        intent = self.parse_query_intent(question)
        category = override_category or intent["category"]
        start_date = override_start_date or intent["start_date"]
        end_date = intent["end_date"]

        # Step 2: Hybrid Retrieval
        retrieved = self.vector_store.search(
            query=question,
            top_k=top_k * 2,
            category=category,
            start_date=start_date,
            end_date=end_date
        )

        # Step 3: Recency-Aware Reranking
        reranked_chunks = self.reranker.rerank(question, retrieved, top_k=top_k)

        # Re-check relevance threshold
        valid_chunks = [c for c in reranked_chunks if c.get("composite_score", 0.0) >= 0.25]

        # Step 4 & 5: Answer Generation & Citations
        if not valid_chunks:
            return {
                "question": question,
                "answer": "I don't have news on that based on the current knowledge base.",
                "citations": [],
                "found_matches": False,
                "intent": intent
            }

        answer_text = self.generate_grounded_answer(question, valid_chunks)

        citations = []
        for c in valid_chunks:
            meta = c["metadata"]
            citations.append({
                "headline": meta.get("headline", ""),
                "source": meta.get("source", ""),
                "url": meta.get("url", "#"),
                "published_date": meta.get("published_date", "")
            })

        return {
            "question": question,
            "answer": answer_text,
            "citations": citations,
            "found_matches": True,
            "intent": intent,
            "chunks_used": len(valid_chunks)
        }

    def generate_daily_briefing(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generates Today's Briefing partitioned by category"""
        briefing = {}
        for domain in ["Tech", "Finance", "Politics"]:
            results = self.vector_store.search(
                query=f"{domain} news policy updates market technology",
                top_k=3,
                category=domain
            )
            items = []
            for r in results:
                meta = r["metadata"]
                items.append({
                    "headline": meta.get("headline", ""),
                    "summary": meta.get("summary", r["content"][:200]),
                    "source": meta.get("source", ""),
                    "url": meta.get("url", "#"),
                    "published_date": meta.get("published_date", "")
                })
            briefing[domain] = items
        return briefing
