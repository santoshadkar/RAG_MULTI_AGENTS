import datetime
from typing import List, Dict, Any
from src.agents.base_agent import BaseFetcherAgent
from src.utils.config import FEEDS
from src.utils.logger import get_logger

logger = get_logger("PoliticsAgent")

POLITICS_KEYWORDS = [
    "government", "parliament", "election", "elections", "policy", "minister",
    "cabinet", "bill", "legislation", "diplomacy", "summit", "treaty", "g20",
    "supreme court", "pib", "foreign ministry", "defence", "bilateral"
]

EXCLUDE_KEYWORDS = ["movie review", "fashion show", "sports fixture", "box office collection"]

FALLBACK_POLITICS_ARTICLES = [
    {
        "article_id": "pol_fb_01",
        "headline": "Cabinet Approves National Clean Energy Infrastructure Bill 2026",
        "body": "The Union Cabinet has approved the comprehensive Clean Energy Infrastructure Bill 2026, allocating ₹45,000 crore for green hydrogen hubs and grid modernization. Prime Minister Narendra Modi chaired the meeting, stating that the legislation will streamline regulatory approvals for solar and wind energy projects across states.",
        "source": "PIB India",
        "url": "https://pib.gov.in/PressReleasePage.aspx?PRID=2026092701",
        "published_date": "2026-09-27",
        "category": "Politics"
    },
    {
        "article_id": "pol_fb_02",
        "headline": "India and EU Sign Historic Bilateral Digital Trade and Data Privacy Agreement",
        "body": "Delegates from India and the European Union signed a comprehensive digital trade pact in New Delhi today. The agreement establishes cross-border data transfer safeguards, mutual recognition of digital identities, and zero-tariff trade on digital software services.",
        "source": "Indian Express",
        "url": "https://indianexpress.com/article/india/india-eu-digital-trade-pact-2026",
        "published_date": "2026-09-26",
        "category": "Politics"
    },
    {
        "article_id": "pol_fb_03",
        "headline": "Parliamentary Standing Committee Submits Report on AI Governance Guidelines",
        "body": "The Parliamentary Standing Committee on Technology and Governance submitted its final recommendations on artificial intelligence regulation. The report advocates for mandatory algorithmic auditing of high-risk applications, deepfake watermarking standards, and specialized AI dispute tribunals.",
        "source": "BBC World",
        "url": "https://bbc.com/news/world-asia-india-20260928-ai-parliament-report",
        "published_date": "2026-09-28",
        "category": "Politics"
    }
]

class PoliticsAgent(BaseFetcherAgent):
    def __init__(self):
        super().__init__(domain="Politics", feeds=FEEDS["Politics"])

    def is_relevant(self, title: str, body: str) -> bool:
        text = f"{title} {body}".lower()
        if any(ex in text for ex in EXCLUDE_KEYWORDS):
            return False
        return any(kw in text for kw in POLITICS_KEYWORDS)

    def fetch_articles(self) -> List[Dict[str, Any]]:
        articles = super().fetch_articles()
        if not articles:
            logger.info("Using curated fallback dataset for Politics domain.")
            articles = FALLBACK_POLITICS_ARTICLES
        return articles
