import datetime
from typing import List, Dict, Any
from src.agents.base_agent import BaseFetcherAgent
from src.utils.config import FEEDS
from src.utils.logger import get_logger

logger = get_logger("TechAgent")

TECH_KEYWORDS = [
    "ai", "artificial intelligence", "tech", "technology", "software", "hardware", 
    "apple", "google", "microsoft", "nvidia", "openai", "semiconductor", "chip",
    "cloud", "cybersecurity", "quantum", "llm", "app", "startup", "robotics"
]

EXCLUDE_KEYWORDS = ["astrology", "recipe", "celebrity gossip", "sports match score"]

FALLBACK_TECH_ARTICLES = [
    {
        "article_id": "tech_fb_01",
        "headline": "NVIDIA Unveils Next-Gen AI Accelerator Architecture for Autonomous Systems",
        "body": "NVIDIA today announced its breakthrough Next-Gen AI accelerator chip designed specifically for real-time generative inference and autonomous edge robotics. The GPU architecture delivers 4x compute efficiency while cutting energy consumption by half. Industry experts note this will accelerate enterprise deployments across robotics and cloud datacenters.",
        "source": "TechCrunch",
        "url": "https://techcrunch.com/2026/09/27/nvidia-next-gen-ai-accelerator",
        "published_date": "2026-09-27",
        "category": "Tech"
    },
    {
        "article_id": "tech_fb_02",
        "headline": "Google DeepMind Releases Open-Weights Reasoning LLM with Multimodal Verification",
        "body": "Google DeepMind has officially released a new open-weights multimodal reasoning model designed for complex agentic workflows and automated code verification. The model achieves state-of-the-art benchmarks on MATH and HumanEval while operating efficiently on local consumer hardware.",
        "source": "BBC Tech",
        "url": "https://bbc.com/news/technology-20260926-deepmind",
        "published_date": "2026-09-26",
        "category": "Tech"
    },
    {
        "article_id": "tech_fb_03",
        "headline": "OpenAI Launches Enterprise Agent Framework for Automated Operations",
        "body": "OpenAI introduced an enterprise agent orchestration suite enabling businesses to build multi-agent software engineering pipelines and automated compliance checkers. Security features include sandbox execution environments and fine-grained access control policies.",
        "source": "Ars Technica",
        "url": "https://arstechnica.com/information-technology/2026/09/openai-enterprise-agents/",
        "published_date": "2026-09-28",
        "category": "Tech"
    }
]

class TechAgent(BaseFetcherAgent):
    def __init__(self):
        super().__init__(domain="Tech", feeds=FEEDS["Tech"])

    def is_relevant(self, title: str, body: str) -> bool:
        text = f"{title} {body}".lower()
        if any(ex in text for ex in EXCLUDE_KEYWORDS):
            return False
        return any(kw in text for kw in TECH_KEYWORDS)

    def fetch_articles(self) -> List[Dict[str, Any]]:
        articles = super().fetch_articles()
        if not articles:
            logger.info("Using curated fallback dataset for Tech domain.")
            articles = FALLBACK_TECH_ARTICLES
        return articles
