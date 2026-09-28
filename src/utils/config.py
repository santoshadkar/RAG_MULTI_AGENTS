import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

CHROMA_PERSIST_DIR = str(os.getenv("CHROMA_PERSIST_DIR", DATA_DIR / "chroma_db"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "news_knowledge_base")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "all-MiniLM-L6-v2")

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 400))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 50))
MAX_ARTICLES_PER_FEED = int(os.getenv("MAX_ARTICLES_PER_FEED", 10))
RECENCY_DECAY_LAMBDA = float(os.getenv("RECENCY_DECAY_LAMBDA", 0.05))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4o-mini")

FEEDS = {
    "Tech": [
        "https://feeds.feedburner.com/TechCrunch/",
        "http://feeds.bbci.co.uk/news/technology/rss.xml",
        "https://news.ycombinator.com/rss",
        "https://arstechnica.com/feed/"
    ],
    "Finance": [
        "https://economictimes.indiatimes.com/rssfeedstopstories.cms",
        "https://www.moneycontrol.com/rss/latestnews.xml",
        "https://www.business-standard.com/rss/finance-103.rss",
        "https://rbi.org.in/rssfeed.xml"
    ],
    "Politics": [
        "https://pib.gov.in/RssMain.aspx?ModId=6",
        "https://indianexpress.com/section/political-pulse/feed/",
        "http://feeds.bbci.co.uk/news/world/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml"
    ]
}
