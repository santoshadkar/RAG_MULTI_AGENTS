# User Stories & Given/When/Then Acceptance Criteria

**Author**: Product Owner  
**Governance Standard**: SAFe Definition of Ready (DoR)  

---

## Story US-01: Multi-Agent Domain Ingestion
**As a** News Analyst,  
**I want** dedicated Tech, Finance, and Politics agents to fetch articles from domain feeds and filter out irrelevant noise,  
**So that** the knowledge base contains only curated, high-quality domain content.

### Acceptance Criteria
- **Given** active RSS/News feed endpoints for Tech, Finance, and Politics,
- **When** the Fetcher Agents execute their scheduled fetch cycle,
- **Then** raw articles are extracted with headline, body, URL, publication date, category, and source.
- **And** articles failing domain relevance rules (e.g. lifestyle in Finance) are filtered out and logged.

---

## Story US-02: Content Processing & Chunking
**As a** RAG System Engineer,  
**I want** raw articles to be cleaned, deduplicated, summarized, entity-extracted, and split into 300–500 token chunks,  
**So that** vector search retrieves precise, coherent contexts.

### Acceptance Criteria
- **Given** a batch of raw articles from domain fetchers,
- **When** the Processing Agent runs,
- **Then** identical or near-duplicate articles across outlets are consolidated into a single article.
- **And** HTML tags/boilerplate are removed, key entities (companies, people, countries) are extracted, and text chunks are generated with length between 300 and 500 tokens.

---

## Story US-03: Vector Store Metadata Indexing
**As a** Knowledge Base Administrator,  
**I want** article chunks embedded and stored in Chroma DB alongside detailed date and category metadata,  
**So that** hybrid vector queries can be filtered efficiently by time range and category.

### Acceptance Criteria
- **Given** processed article chunks with metadata,
- **When** the Vector Store ingests the chunks,
- **Then** embeddings are created using sentence-transformers and persisted in Chroma DB.
- **And** queries with filter parameters (`category == 'Finance'`, `published_date >= '2026-09-21'`) correctly restrict retrieval candidates.

---

## Story US-04: Recency-Aware Grounded RAG Query Engine
**As an** Executive User,  
**I want** to ask questions like "What did the RBI announce this week and how did markets react?",  
**So that** I receive accurate, recency-boosted answers strictly grounded in retrieved articles with clear source citations.

### Acceptance Criteria
- **Given** a user natural language query with time references (e.g., "this week", "today"),
- **When** the RAG Query Engine processes the query,
- **Then** it interprets time range and category filters, performs hybrid vector search, and reranks results giving higher weights to recent dates.
- **And** it generates an answer strictly using retrieved context with inline citations `[Source Name, YYYY-MM-DD](URL)`.
- **And** if no relevant news is found, it returns `"I don't have news on that."` without hallucinating.

---

## Story US-05: Interactive Streamlit Dashboard & Briefings
**As a** Business User,  
**I want** a web interface with chat capabilities, domain filters, date pickers, and an automated "Today's Briefing" panel,  
**So that** I can easily explore current news and review morning summaries.

### Acceptance Criteria
- **Given** a running Streamlit app,
- **When** the user accesses the web dashboard,
- **Then** they can chat with the assistant, filter by domain/date, view automatically generated daily briefings, and inspect agent status metrics.
