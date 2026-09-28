# PI Planning Board & Program Increment Roadmap

**Program Increment**: PI-2026-Q3 (AI News Intelligence Platform)  
**Release Train**: Agile Release Train (ART-01: News & Intelligence Engineering)  
**Release Train Engineer**: RTE Lead  

---

## 1. Feature Allocation Matrix across Sprints

| Feature ID | Feature Name | Agile Team | Sprint 1 (Inception & Governance) | Sprint 2 (Fetchers & Processing) | Sprint 3 (Vector Engine & RAG) | Sprint 4 (Streamlit UI & Release) |
|---|---|---|---|---|---|---|
| **FEAT-101** | Multi-Source Fetcher Agents (Tech, Finance, Politics) | Team Alpha | Design RSS & API schemas | Build fetchers & domain filters | Test real feed ingestion | Production polish |
| **FEAT-102** | Processing Agent & Chunking Pipeline | Team Alpha | Data contracts | Deduplication & entity extractor | 300-500 token chunker | Edge case validation |
| **FEAT-103** | Vector Store & Embeddings | Team Beta | Embeddings selection | Setup Chroma persistence | Hybrid search & recency index | Performance tuning |
| **FEAT-104** | Time & Category-Aware RAG Engine | Team Beta | RAG spec & prompt engineering | Intent parser | Recency reranking & citations | Fallback & evaluation |
| **FEAT-105** | Streamlit Chat & Briefing Interface | Team Gamma | UI Wireframes & layout | Briefing generator component | Interactive Chat & filters | QA Audit & CAB Signoff |

---

## 2. ART Cross-Team Dependencies

```
[FEAT-101: Fetchers] ───► [FEAT-102: Processing Agent] ───► [FEAT-103: Vector Store] ───► [FEAT-104: RAG Engine] ───► [FEAT-105: UI]
```

- **Dependency 1**: Processing Agent depends on Fetcher Agents standardized payload format (headline, body, date, source, category, url).
- **Dependency 2**: Vector Store depends on Processing Agent metadata schema and chunk outputs.
- **Dependency 3**: RAG Query Engine depends on Chroma DB query interface with category and date filtering.
- **Dependency 4**: Streamlit Dashboard depends on Orchestrator status API and RAG engine query function.

---

## 3. ROAM Risk Matrix

| Risk ID | Risk Description | Category | Action | Owner | Mitigation / Resolution |
|---|---|---|---|---|---|
| **RSK-01** | External RSS feeds or News API rate limits causing fetch failures | High | **Mitigated** | Team Alpha | Implement exponential backoff retries and local fallback RSS cache. |
| **RSK-02** | Hallucination in LLM answers regarding real-time news | High | **Mitigated** | Team Beta | Enforce strict grounded prompt constraint ("Say 'I don't have news on that' if not found"). |
| **RSK-03** | High latency in hybrid vector search and reranking | Medium | **Owned** | Team Beta | Pre-filter Chroma DB by category & date before top-k reranking. |
| **RSK-04** | Duplicate stories across 20+ news outlets | Medium | **Resolved** | Team Alpha | Cross-source similarity deduplication (hash & normalized title matching). |

---

## 4. PI Objectives & Commitments
- **Business Goal**: Enable business owners to ask natural language questions about today's news with grounded responses, source links, and dates.
- **Velocity Target**: 40 Story Points across Sprints 1-4.
- **PI Gate Approval**: Signed off by RTE Lead.
