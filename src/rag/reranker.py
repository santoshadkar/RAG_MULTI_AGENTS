import math
import datetime
from typing import List, Dict, Any
from rank_bm25 import BM25Okapi
from src.utils.config import RECENCY_DECAY_LAMBDA
from src.utils.logger import get_logger

logger = get_logger("Reranker")

class RecencyReranker:
    def __init__(self, lambda_decay: float = RECENCY_DECAY_LAMBDA):
        self.lambda_decay = lambda_decay

    def calculate_recency_score(self, pub_date_str: str, reference_date: datetime.date) -> float:
        try:
            pub_date = datetime.datetime.strptime(pub_date_str, "%Y-%m-%d").date()
            days_diff = (reference_date - pub_date).days
            if days_diff < 0:
                days_diff = 0
            # Exponential decay: e^(-lambda * days)
            return math.exp(-self.lambda_decay * days_diff)
        except Exception:
            return 0.5

    def rerank(self, query: str, results: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        if not results:
            return []

        # Tokenize for BM25
        corpus = [r["content"].lower().split() for r in results]
        tokenized_query = query.lower().split()
        
        bm25 = BM25Okapi(corpus)
        bm25_scores = bm25.get_scores(tokenized_query)
        max_bm25 = max(bm25_scores) if max(bm25_scores) > 0 else 1.0
        normalized_bm25 = [s / max_bm25 for s in bm25_scores]

        ref_date = datetime.date.today()

        reranked = []
        for idx, item in enumerate(results):
            vec_sim = item.get("similarity", 0.5)
            bm25_score = normalized_bm25[idx]
            pub_date_str = item["metadata"].get("published_date", "")
            recency_weight = self.calculate_recency_score(pub_date_str, ref_date)

            # Composite Score formula
            final_score = (0.45 * vec_sim) + (0.35 * bm25_score) + (0.20 * recency_weight)
            
            item_copy = dict(item)
            item_copy["composite_score"] = round(final_score, 4)
            item_copy["recency_boost"] = round(recency_weight, 4)
            reranked.append(item_copy)

        reranked.sort(key=lambda x: x["composite_score"], reverse=True)
        return reranked[:top_k]
