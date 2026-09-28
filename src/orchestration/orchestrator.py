import datetime
import time
from typing import Dict, Any, List
from src.agents.tech_agent import TechAgent
from src.agents.finance_agent import FinanceAgent
from src.agents.politics_agent import PoliticsAgent
from src.agents.processing_agent import ProcessingAgent
from src.knowledge_base.vector_store import NewsVectorStore
from src.utils.logger import get_logger

logger = get_logger("Orchestrator")

class NewsOrchestrator:
    def __init__(self):
        self.tech_agent = TechAgent()
        self.finance_agent = FinanceAgent()
        self.politics_agent = PoliticsAgent()
        self.processing_agent = ProcessingAgent()
        self.vector_store = NewsVectorStore()
        self.execution_history: List[Dict[str, Any]] = []

    def run_pipeline(self, target_category: str = "all") -> Dict[str, Any]:
        start_time = time.time()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logger.info(f"Starting News Orchestrator pipeline run for category: {target_category}")

        raw_articles = []
        domain_counts = {}

        # 1. Fetcher Agents Execution
        if target_category in ["all", "Tech"]:
            try:
                tech_news = self.tech_agent.fetch_articles()
                raw_articles.extend(tech_news)
                domain_counts["Tech"] = len(tech_news)
            except Exception as e:
                logger.error(f"TechAgent failed: {e}")
                domain_counts["Tech"] = 0

        if target_category in ["all", "Finance"]:
            try:
                fin_news = self.finance_agent.fetch_articles()
                raw_articles.extend(fin_news)
                domain_counts["Finance"] = len(fin_news)
            except Exception as e:
                logger.error(f"FinanceAgent failed: {e}")
                domain_counts["Finance"] = 0

        if target_category in ["all", "Politics"]:
            try:
                pol_news = self.politics_agent.fetch_articles()
                raw_articles.extend(pol_news)
                domain_counts["Politics"] = len(pol_news)
            except Exception as e:
                logger.error(f"PoliticsAgent failed: {e}")
                domain_counts["Politics"] = 0

        # 2. Processing & Chunking Pipeline
        processed_chunks = self.processing_agent.process_articles(raw_articles)

        # 3. Knowledge Base Ingestion
        self.vector_store.add_chunks(processed_chunks)

        duration = round(time.time() - start_time, 2)
        run_record = {
            "timestamp": timestamp,
            "status": "SUCCESS",
            "category": target_category,
            "raw_articles_fetched": len(raw_articles),
            "chunks_ingested": len(processed_chunks),
            "domain_breakdown": domain_counts,
            "execution_time_sec": duration
        }
        self.execution_history.append(run_record)
        logger.info(f"Pipeline completed in {duration}s. Chunks stored: {len(processed_chunks)}")
        return run_record

    def get_run_history(self) -> List[Dict[str, Any]]:
        return self.execution_history
