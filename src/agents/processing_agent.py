import re
import hashlib
from typing import List, Dict, Any
from src.utils.config import CHUNK_SIZE, CHUNK_OVERLAP
from src.utils.logger import get_logger

logger = get_logger("ProcessingAgent")

# Known entity dictionary patterns
ORG_ENTITIES = [
    "RBI", "SEBI", "NVIDIA", "Google", "DeepMind", "OpenAI", "Federal Reserve", "Fed",
    "BSE", "NSE", "EU", "European Union", "Cabinet", "Parliament", "Union Cabinet"
]

PERSON_ENTITIES = [
    "Das", "Shaktikanta Das", "Powell", "Jerome Powell", "Narendra Modi", "Modi"
]

LOCATION_ENTITIES = [
    "India", "US", "USA", "New Delhi", "Washington", "Europe"
]

class ProcessingAgent:
    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def deduplicate(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        unique_articles = []
        seen_titles = set()
        seen_hashes = set()

        for article in articles:
            title = article["headline"].strip().lower()
            # Normalize title for cross-outlet comparison
            norm_title = re.sub(r'[^a-z0-9]', '', title)
            
            # Content signature
            body_snippet = article["body"][:100].lower()
            content_hash = hashlib.md5(body_snippet.encode('utf-8')).hexdigest()

            if norm_title in seen_titles or content_hash in seen_hashes:
                logger.info(f"Duplicate article detected and removed: '{article['headline']}'")
                continue

            seen_titles.add(norm_title)
            seen_hashes.add(content_hash)
            unique_articles.append(article)

        logger.info(f"Deduplication complete. {len(unique_articles)} unique articles remaining from {len(articles)} total.")
        return unique_articles

    def extract_entities(self, text: str) -> List[str]:
        entities = set()
        for org in ORG_ENTITIES:
            if re.search(r'\b' + re.escape(org) + r'\b', text, re.IGNORECASE):
                entities.add(org)
        for person in PERSON_ENTITIES:
            if re.search(r'\b' + re.escape(person) + r'\b', text, re.IGNORECASE):
                entities.add(person)
        for loc in LOCATION_ENTITIES:
            if re.search(r'\b' + re.escape(loc) + r'\b', text, re.IGNORECASE):
                entities.add(loc)
        
        # Capitalized multi-word proper nouns heuristic
        matches = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b', text)
        for m in matches:
            if len(m) > 3 and m not in ["Monetary Policy", "Clean Energy"]:
                entities.add(m)

        return list(entities)

    def generate_summary(self, body: str, max_sentences: int = 2) -> str:
        # Simple extractive summarizer taking key opening sentences
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', body) if len(s.strip()) > 15]
        if not sentences:
            return body[:200]
        return " ".join(sentences[:max_sentences])

    def chunk_text(self, text: str) -> List[str]:
        words = text.split()
        if len(words) <= self.chunk_size:
            return [text]

        chunks = []
        start = 0
        while start < len(words):
            end = min(start + self.chunk_size, len(words))
            chunk = " ".join(words[start:end])
            chunks.append(chunk)
            if end == len(words):
                break
            start += self.chunk_size - self.chunk_overlap
        return chunks

    def process_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        deduped = self.deduplicate(articles)
        processed_chunks = []

        for article in deduped:
            summary = self.generate_summary(article["body"])
            entities = self.extract_entities(f"{article['headline']} {article['body']}")
            chunks = self.chunk_text(article["body"])

            for idx, chunk in enumerate(chunks):
                chunk_obj = {
                    "chunk_id": f"{article['article_id']}_c{idx}",
                    "article_id": article["article_id"],
                    "headline": article["headline"],
                    "content": chunk,
                    "summary": summary,
                    "entities": ", ".join(entities),
                    "source": article["source"],
                    "url": article["url"],
                    "published_date": article["published_date"],
                    "category": article["category"]
                }
                processed_chunks.append(chunk_obj)

        logger.info(f"Processing complete. Generated {len(processed_chunks)} metadata-enriched chunks.")
        return processed_chunks
