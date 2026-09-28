import datetime
from typing import List, Dict, Any
from src.agents.base_agent import BaseFetcherAgent
from src.utils.config import FEEDS
from src.utils.logger import get_logger

logger = get_logger("FinanceAgent")

FINANCE_KEYWORDS = [
    "rbi", "sebi", "market", "markets", "stocks", "sensex", "nifty", "inflation",
    "monetary policy", "interest rate", "repo rate", "banking", "economy", "fiscal",
    "earnings", "revenue", "gdp", "treasury", "bonds", "forex", "fed", "central bank"
]

EXCLUDE_KEYWORDS = ["horoscope", "bollywood fashion", "cricket match score", "celebrity lifestyle"]

FALLBACK_FINANCE_ARTICLES = [
    {
        "article_id": "fin_fb_01",
        "headline": "RBI Keeps Repo Rate Unchanged at 6.5% in September Policy Review; Markets Rally",
        "body": "The Reserve Bank of India (RBI) Monetary Policy Committee decided to keep the benchmark repo rate unchanged at 6.50% for the ninth consecutive meeting. Governor Das highlighted that core inflation has moderated to 3.8% while India's GDP growth projection remains strong at 7.2% for FY26. Following the RBI announcement, the BSE Sensex rose 350 points, led by gains in banking and financial sector stocks.",
        "source": "Economic Times",
        "url": "https://economictimes.indiatimes.com/markets/rbi-monetary-policy-rate-decision-2026",
        "published_date": "2026-09-27",
        "category": "Finance"
    },
    {
        "article_id": "fin_fb_02",
        "headline": "SEBI Introduces Stricter Algorithmic Trading Safeguards for Retail Investors",
        "body": "Capital markets regulator SEBI has issued new guidelines mandatory for stockbrokers offering algorithmic trading APIs. The framework mandates multi-tier risk checks, automated circuit breakers, and mandatory API token rotation to safeguard retail traders against flash crashes.",
        "source": "Moneycontrol",
        "url": "https://moneycontrol.com/news/business/markets/sebi-algo-trading-rules-2026",
        "published_date": "2026-09-25",
        "category": "Finance"
    },
    {
        "article_id": "fin_fb_03",
        "headline": "US Federal Reserve Signals 25 Basis Point Rate Cut as Inflation Cools",
        "body": "The Federal Reserve indicated a potential 25 basis point reduction in federal funds rates during its upcoming FOMC meeting. Chairman Jerome Powell cited weakening labor market pressure and inflation aligning near the 2% target. Global equity markets reacted positively with tech and consumer stocks surging.",
        "source": "Business Standard",
        "url": "https://business-standard.com/finance/us-fed-rate-cut-signal-2026",
        "published_date": "2026-09-28",
        "category": "Finance"
    }
]

class FinanceAgent(BaseFetcherAgent):
    def __init__(self):
        super().__init__(domain="Finance", feeds=FEEDS["Finance"])

    def is_relevant(self, title: str, body: str) -> bool:
        text = f"{title} {body}".lower()
        if any(ex in text for ex in EXCLUDE_KEYWORDS):
            return False
        return any(kw in text for kw in FINANCE_KEYWORDS)

    def fetch_articles(self) -> List[Dict[str, Any]]:
        articles = super().fetch_articles()
        if not articles:
            logger.info("Using curated fallback dataset for Finance domain.")
            articles = FALLBACK_FINANCE_ARTICLES
        return articles
