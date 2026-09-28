from sentence_transformers import SentenceTransformer
from typing import List
from src.utils.config import EMBEDDING_MODEL_NAME
from src.utils.logger import get_logger

logger = get_logger("Embeddings")

class EmbeddingEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingEngine, cls).__new__(cls)
            logger.info(f"Initializing SentenceTransformer embedding model: {EMBEDDING_MODEL_NAME}")
            cls._instance.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        return cls._instance

    def encode(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    def encode_single(self, text: str) -> List[float]:
        return self.encode([text])[0]
