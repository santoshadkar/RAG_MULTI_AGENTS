import re
import datetime
import hashlib
import feedparser
from bs4 import BeautifulSoup
import requests
from typing import List, Dict, Any
from src.utils.logger import get_logger
from src.utils.config import MAX_ARTICLES_PER_FEED

logger = get_logger("BaseAgent")

class BaseFetcherAgent:
    def __init__(self, domain: str, feeds: List[str]):
        self.domain = domain
        self.feeds = feeds

    def clean_html(self, raw_html: str) -> str:
        if not raw_html:
            return ""
        soup = BeautifulSoup(raw_html, "html.parser")
        text = soup.get_text(separator=" ")
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def parse_date(self, entry: Dict[str, Any]) -> str:
        published = entry.get("published") or entry.get("updated") or entry.get("pubDate")
        if published:
            try:
                dt = datetime.datetime.fromtimestamp(
                    datetime.datetime.strptime(published[:25], "%a, %d %b %Y %H:%M:%S").timestamp()
                )
                return dt.strftime("%Y-%m-%d")
            except Exception:
                pass
            try:
                # ISO format or fuzzy search
                match = re.search(r'\d{4}-\d{2}-\d{2}', str(published))
                if match:
                    return match.group(0)
            except Exception:
                pass
        return datetime.date.today().strftime("%Y-%m-%d")

    def is_relevant(self, title: str, body: str) -> bool:
        """Domain specific filter override in subclass"""
        return True

    def fetch_articles(self) -> List[Dict[str, Any]]:
        articles = []
        for feed_url in self.feeds:
            try:
                logger.info(f"Fetching {self.domain} feed from: {feed_url}")
                parsed = feedparser.parse(feed_url)
                count = 0
                for entry in parsed.entries:
                    if count >= MAX_ARTICLES_PER_FEED:
                        break
                    
                    title = entry.get("title", "").strip()
                    summary = entry.get("summary", "") or entry.get("description", "")
                    content_list = entry.get("content", [])
                    full_body = summary
                    if content_list and isinstance(content_list, list):
                        full_body += " " + content_list[0].get("value", "")

                    clean_title = self.clean_html(title)
                    clean_body = self.clean_html(full_body)

                    if not clean_title or len(clean_body) < 50:
                        continue

                    if not self.is_relevant(clean_title, clean_body):
                        logger.info(f"Filtering out irrelevant article: '{clean_title}'")
                        continue

                    pub_date = self.parse_date(entry)
                    link = entry.get("link", "#")
                    
                    article_id = hashlib.md5(f"{clean_title}_{pub_date}".encode('utf-8')).hexdigest()[:12]

                    articles.append({
                        "article_id": f"{self.domain.lower()}_{article_id}",
                        "headline": clean_title,
                        "body": clean_body,
                        "source": parsed.feed.get("title", feed_url.split('/')[2]),
                        "url": link,
                        "published_date": pub_date,
                        "category": self.domain
                    })
                    count += 1
            except Exception as e:
                logger.error(f"Error fetching from feed {feed_url}: {e}")

        logger.info(f"{self.domain} Agent collected {len(articles)} relevant articles.")
        return articles
