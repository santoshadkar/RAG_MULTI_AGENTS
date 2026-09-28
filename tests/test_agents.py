import pytest
from src.agents.tech_agent import TechAgent
from src.agents.finance_agent import FinanceAgent
from src.agents.politics_agent import PoliticsAgent

def test_tech_agent_relevance():
    agent = TechAgent()
    assert agent.is_relevant("New AI Model Released by OpenAI", "The LLM software is faster.") is True
    assert agent.is_relevant("Best Chocolate Cake Recipe", "Mix flour and sugar in a bowl.") is False

def test_finance_agent_relevance():
    agent = FinanceAgent()
    assert agent.is_relevant("RBI Monetary Policy Rate Unchanged", "Governor Das announced repo rate stays at 6.5%.") is True
    assert agent.is_relevant("Horoscope Predictions for Aries", "Today is a lucky day for stars.") is False

def test_politics_agent_relevance():
    agent = PoliticsAgent()
    assert agent.is_relevant("Union Cabinet Approves Energy Bill", "Parliament passed green hydrogen legislation.") is True
    assert agent.is_relevant("Movie Box Office Collection", "The blockbuster made 100 crores.") is False

def test_fetch_articles():
    tech_agent = TechAgent()
    articles = tech_agent.fetch_articles()
    assert len(articles) > 0
    assert "headline" in articles[0]
    assert "published_date" in articles[0]
    assert articles[0]["category"] == "Tech"
