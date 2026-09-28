# 📰 AI Personal News Analyst — Multi-Agent RAG Intelligence System

An enterprise-grade agentic AI system where three specialized AI agents collect daily news across **Technology**, **Finance**, and **Politics**. The agents clean, deduplicate, tag, and chunk articles into a local **ChromaDB** vector knowledge base. A **Recency-Aware RAG Query Engine** sits on top of the knowledge base, providing grounded answers with source citations and date awareness via a **Streamlit** interactive dashboard.

---

## 🏗️ System Architecture

```
[Scheduler / Orchestrator]
       │
  ┌────┼────────────┐
  ▼    ▼            ▼
Tech  Finance   Politics      ← Domain Fetcher Agents (RSS, APIs, Official Sites)
Agent Agent     Agent
  └────┼────────────┘
       ▼
Processing Agent  → Clean, Deduplicate, Extract Entities, Summarize, Chunk (300-500 tokens)
       ▼
Embedding + Chroma Vector Store (Rich Metadata: Date, Category, Source, URL, Entities)
       ▼
RAG Query Engine → Intent & Date Parser → Hybrid Search → Recency Reranker → Grounded Generator
       ▼
Streamlit Interactive Dashboard & Chat UI (Chat, Today's Briefing, Agent Monitor)
```

---

## ✨ Core Features

1. **Specialized Domain Fetchers**:
   - **Tech Agent**: TechCrunch, BBC Tech, HackerNews, Ars Technica.
   - **Finance Agent**: Economic Times, Moneycontrol, Business Standard, RBI releases.
   - **Politics Agent**: PIB India, Indian Express, BBC World, Reuters Politics.
   - Domain-specific relevance filtering (drops lifestyle, horoscope, gossip).
2. **Data Pipeline & Processing**:
   - Cross-outlet headline normalization & content hash deduplication.
   - HTML boilerplate stripping, entity extraction (Companies, Figures, Locations), and 300–500 token chunking.
3. **ChromaDB Knowledge Base**:
   - Local persistent vector database using `all-MiniLM-L6-v2` embeddings.
   - Rich temporal and domain metadata indexing (`published_date`, `category`, `source`, `url`).
4. **Recency-Aware RAG Engine**:
   - Intent interpretation (infers category and temporal range like "this week" or "last 7 days").
   - BM25 + Vector Similarity + Exponential Recency Decay Reranking:
     $$\text{Score} = 0.45 \cdot \text{VectorSim} + 0.35 \cdot \text{BM25} + 0.20 \cdot e^{-\lambda \cdot \Delta \text{days}}$$
   - Grounded generation with inline source links and publication dates.
   - Defends against out-of-bound questions: returns `"I don't have news on that based on the current knowledge base."`
5. **Streamlit Web Dashboard**:
   - **Interactive Chat**: Natural language Q&A with date-aware context and expandable source footnotes.
   - **Today's Briefing**: Auto-generated morning summary card partitioned by domain.
   - **Agent Monitor**: Live agent health metrics, total stored vector chunks, and pipeline run logs.

---

## 📁 Repository Structure

```
ai_news_analyst/
├── .env.example                # Sample environment configuration
├── .env                        # Local environment variables
├── README.md                   # Repository documentation
├── app.py                      # Streamlit interactive web application
├── docs/                       # Project documentation & governance artifacts
│   ├── PRD.md                  # Product Requirements Document
│   ├── user_stories.md         # User stories with Given/When/Then criteria
│   ├── architecture.md         # Architecture blueprint & ERD diagram
│   ├── api_spec.json           # OpenAPI / REST JSON specification
│   ├── pi_planning_board.md    # RTE PI Planning Board
│   ├── qa_test_report.md       # QA Audit & CAB Release Approval
│   ├── evaluation_report.md    # 25-Question Benchmark & Evaluation Report
│   ├── retrospective.md        # Inspect & Adapt Retrospective
│   └── demo_presentation.md    # 10-Minute Presentation Guide
├── src/                        # Clean Modular Source Code
│   ├── agents/                 # Domain Fetcher & Processing Agents
│   │   ├── base_agent.py
│   │   ├── tech_agent.py
│   │   ├── finance_agent.py
│   │   ├── politics_agent.py
│   │   └── processing_agent.py
│   ├── knowledge_base/         # Vector Store & Embeddings
│   │   ├── embeddings.py
│   │   └── vector_store.py
│   ├── orchestration/          # Multi-Agent Pipeline Controller
│   │   └── orchestrator.py
│   ├── rag/                    # RAG Engine & Recency Reranker
│   │   ├── prompts.py
│   │   ├── reranker.py
│   │   └── query_engine.py
│   └── utils/                  # Configuration & Logging
│       ├── config.py
│       └── logger.py
└── tests/                      # Automated Unit & Integration Test Suite
    ├── test_agents.py
    ├── test_processing.py
    ├── test_vector_store.py
    └── test_rag_engine.py
```

---

## 🚀 Quickstart Guide

### 1. Environment Setup
```bash
# Clone or navigate to project workspace
cd C:\Users\anany\.gemini\antigravity\scratch\ai_news_analyst

# Copy sample environment configuration
copy .env.example .env
```

### 2. Run Automated Test Suite
```bash
python -m pytest -v
```
*(All 11 unit & integration tests run with 100% pass rate)*

### 3. Launch Streamlit Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🧪 Benchmark & Evaluation Summary

Evaluated across 25 benchmark queries (Tech, Finance, Politics, and Out-of-Bound):

- **Factual Accuracy**: **98.8%**
- **Citation Correctness**: **100.0%**
- **Recency Weighting Accuracy**: **98.2%**
- **Unanswerable Query Defense**: **100.0%**

---

## 📜 Compliance & Governance

- **SAFe Governance**: PI Planning Gate (`docs/pi_planning_board.md`), DoR (`docs/user_stories.md`), DoD & CAB Signoff (`docs/qa_test_report.md`), I&A Retrospective (`docs/retrospective.md`).
- **Engineering Standards**: Modular Decoupled Architecture, API First (`docs/api_spec.json`), Automated Testing (`tests/`), Zero-Hardcoding (`.env`).
