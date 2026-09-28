import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from src.knowledge_base.embeddings import EmbeddingEngine
from src.utils.config import CHROMA_PERSIST_DIR, COLLECTION_NAME
from src.utils.logger import get_logger

logger = get_logger("VectorStore")

class NewsVectorStore:
    def __init__(self, persist_dir: str = CHROMA_PERSIST_DIR, collection_name: str = COLLECTION_NAME):
        self.persist_dir = persist_dir
        self.collection_name = collection_name
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.embedding_engine = EmbeddingEngine()
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"Connected to ChromaDB at {self.persist_dir}, collection: {self.collection_name}")

    def add_chunks(self, chunks: List[Dict[str, Any]]):
        if not chunks:
            logger.info("No chunks provided to add_chunks.")
            return

        ids = [c["chunk_id"] for c in chunks]
        documents = [f"{c['headline']}\n{c['content']}" for c in chunks]
        metadatas = [
            {
                "article_id": c["article_id"],
                "headline": c["headline"],
                "source": c["source"],
                "url": c["url"],
                "published_date": c["published_date"],
                "category": c["category"],
                "entities": c.get("entities", ""),
                "summary": c.get("summary", "")
            }
            for c in chunks
        ]

        logger.info(f"Generating embeddings for {len(chunks)} chunks...")
        embeddings = self.embedding_engine.encode(documents)

        self.collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        logger.info(f"Successfully upserted {len(chunks)} chunks to ChromaDB.")

    def search(
        self,
        query: str,
        top_k: int = 10,
        category: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        query_embedding = self.embedding_engine.encode_single(query)

        where_clause = {}
        conditions = []

        if category and category != "all" and category != "All":
            conditions.append({"category": category})
        if start_date:
            conditions.append({"published_date": {"$gte": start_date}})
        if end_date:
            conditions.append({"published_date": {"$lte": end_date}})

        if len(conditions) == 1:
            where_clause = conditions[0]
        elif len(conditions) > 1:
            where_clause = {"$and": conditions}

        kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": top_k
        }
        if where_clause:
            kwargs["where"] = where_clause

        try:
            results = self.collection.query(**kwargs)
        except Exception as e:
            logger.error(f"Error querying ChromaDB with filter {where_clause}: {e}. Retrying without filter.")
            kwargs.pop("where", None)
            results = self.collection.query(**kwargs)

        search_results = []
        if results and "documents" in results and results["documents"]:
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            distances = results["distances"][0] if "distances" in results else [0.0]*len(docs)

            for doc, meta, dist in zip(docs, metas, distances):
                similarity_score = round(1.0 - dist, 4) if dist <= 1.0 else round(1.0 / (1.0 + dist), 4)
                search_results.append({
                    "content": doc,
                    "metadata": meta,
                    "similarity": similarity_score
                })

        return search_results

    def get_stats(self) -> Dict[str, Any]:
        count = self.collection.count()
        return {
            "total_chunks": count,
            "collection_name": self.collection_name,
            "persist_dir": self.persist_dir
        }
