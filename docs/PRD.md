# Product Requirements Document (PRD): AI News Intelligence System

**Product Owner**: Product Owner / Business Analyst  
**Version**: 1.0.0  
**Status**: Approved  

---

## 1. Executive Summary
Business owners and decision-makers face information overload, unable to consume hundreds of daily news stories across Technology, Finance, and Politics. Existing LLM chatbots either lack real-time context or produce ungrounded answers without citations. 

The **AI News Intelligence System** deploys 3 specialized domain fetcher agents (Tech, Finance, Politics), a processing and deduplication pipeline, a Chroma vector knowledge base, a date- and category-aware RAG query engine, and a Streamlit chat interface with automated daily briefings.

---

## 2. Core Functional Requirements

### FR-1: Specialized Domain Fetchers
- **Tech Agent**: Ingests technology news (AI, software, hardware, startups) from TechCrunch, BBC Tech, HackerNews, Ars Technica. Drops non-tech content.
- **Finance Agent**: Ingests markets, monetary policy (RBI, SEBI, Fed), earnings, macroeconomics from Economic Times, Moneycontrol, Business Standard, RBI press releases. Drops lifestyle/opinion pieces.
- **Politics Agent**: Ingests public policy, governance, elections, international relations from PIB India, Reuters Politics, BBC World, Indian Express. Drops gossip/tabloid news.

### FR-2: Orchestrator
- Schedules automated runs (hourly/daily).
- Manages agent lifecycles, retries failed feed requests, logs run metrics, and updates collection status.

### FR-3: Processing Pipeline
- Deduplication across outlets (titles, hash matching).
- Strips HTML boilerplate and advertising fluff.
- Summarizes articles into concise bullet summaries.
- Extracts entities (Companies, Key Figures, Organizations, Countries).
- Tags articles by domain and splits them into 300–500 token chunks.

### FR-4: Vector Knowledge Base
- Stores embeddings locally using ChromaDB.
- Attaches rich metadata to each chunk: `article_id`, `headline`, `url`, `source`, `category`, `published_date`, `entities`, `summary`.

### FR-5: RAG Query Engine
- **Intent Analysis**: Extracts target category and temporal context (e.g. "this week", "last 7 days").
- **Hybrid Search**: Metadata filtering combined with vector similarity search.
- **Recency-Aware Reranking**: Boosts scores of newer articles so recent news is prioritized.
- **Grounded Answer Generation**: Synthesizes response ONLY using retrieved context.
- **Citations & Fallback**: Formats footnotes/links with dates. Responds `"I don't have news on that"` if search yields no relevant match.

### FR-6: Interactive Streamlit UI
- **Chat Interface**: Natural language Q&A with date-aware context and inline clickable source citations.
- **Category & Date Filters**: Sidebar controls to narrow focus to specific domains or date ranges.
- **Today's Briefing**: Auto-generated morning summary partitioned by Tech, Finance, and Politics.
- **Agent Monitor Dashboard**: Real-time status of fetch agents, total stored chunks, and manual trigger controls.

---

## 3. Non-Functional Requirements
- **Latency**: Query response under 3 seconds.
- **Accuracy & Groundedness**: 0% hallucination on missing topics; strict citations.
- **Zero-Hardcoding**: API keys, feed endpoints, vector DB settings configurable via `.env`.
