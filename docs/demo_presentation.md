# 10-Minute Demo & Presentation Guide

**Project**: AI Personal News Analyst — Multi-Agent RAG Intelligence System  
**Presenter**: Engineering Team  

---

## Slide & Demo Breakdown (10 Minutes Total)

### Minute 0:00 – 1:30 | The Problem & Vision
- **Problem**: Business owners & decision-makers face news overload across 100+ sources daily. General chatbots lack real-time news context and hallucinate sources.
- **Solution**: Personal AI News Analyst with 3 specialized domain fetcher agents (Tech, Finance, Politics), a vector knowledge base, and a date-aware RAG query engine.

### Minute 1:30 – 3:30 | System Architecture
- **Multi-Agent Orchestration**: Tech, Finance, and Politics Agents collect and filter domain feeds.
- **Processing Agent**: Normalizes text, deduplicates cross-outlet articles, extracts entities (companies, people, countries), and creates 300–500 token chunks.
- **Knowledge Base & Recency Reranker**: Chroma DB vector store with temporal metadata filtering and BM25 + Recency decay reranking.

### Minute 3:30 – 7:30 | Live Product Walkthrough
- **Tab 1: Interactive Chat**:
  - Ask: *"What did the RBI announce this week and how did markets react?"*
  - Show grounded answer citing Economic Times with date (September 27, 2026) and Sensex rally data.
  - Ask out-of-bound question: *"What is the secret recipe for Martian space pie?"*
  - Show zero-hallucination response: *"I don't have news on that based on the current knowledge base."*
- **Tab 2: Today's Briefing**:
  - Show automatically generated morning summary partitioned into Tech, Finance, and Politics cards.
- **Tab 3: Agent Orchestration & Monitor**:
  - Show active agent health indicators and pipeline run logs.

### Minute 7:30 – 9:00 | Evaluation & Benchmarks
- Benchmark results across 25 test questions:
  - 98.8% Factual Accuracy
  - 100% Citation Correctness
  - 100% Unanswerable Query Defense

### Minute 9:00 – 10:00 | Q&A & Conclusion
- Summary of core agentic AI skills covered: multi-agent orchestration, data pipelines, vector search, prompt design, and production Streamlit UI.
