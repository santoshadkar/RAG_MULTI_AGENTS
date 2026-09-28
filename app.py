import streamlit as st
import datetime
import pandas as pd
from src.orchestration.orchestrator import NewsOrchestrator
from src.rag.query_engine import RAGQueryEngine
from src.utils.logger import get_logger

logger = get_logger("StreamlitApp")

# Page Configuration
st.set_page_config(
    page_title="AI News Analyst - Multi-Agent RAG Intelligence",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .source-card {
        background-color: #F8FAFC;
        border-left: 4px solid #3B82F6;
        padding: 0.8rem 1rem;
        border-radius: 4px;
        margin-bottom: 0.5rem;
    }
    .citation-tag {
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .briefing-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1.2rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = NewsOrchestrator()

if "query_engine" not in st.session_state:
    st.session_state.query_engine = RAGQueryEngine(
        vector_store=st.session_state.orchestrator.vector_store
    )

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "auto_ingested" not in st.session_state:
    # Pre-populate knowledge base on first load
    with st.spinner("Initializing AI Agents & Knowledge Base..."):
        st.session_state.orchestrator.run_pipeline("all")
        st.session_state.auto_ingested = True

# App Title Header
st.markdown('<div class="main-header">📰 Personal AI News Analyst</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-Agent Intelligence System grounded in verified Tech, Finance & Politics news</div>', unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.header("⚙️ Controls & Filters")

category_filter = st.sidebar.selectbox(
    "Category Domain Filter",
    options=["All", "Tech", "Finance", "Politics"],
    index=0
)

st.sidebar.subheader("📅 Date Range Filter")
today = datetime.date.today()
seven_days_ago = today - datetime.timedelta(days=7)

start_date_val = st.sidebar.date_input("Start Date", value=seven_days_ago)
end_date_val = st.sidebar.date_input("End Date", value=today)

st.sidebar.markdown("---")
st.sidebar.subheader("🔄 Ingestion Controls")
if st.sidebar.button("Fetch & Process Latest News"):
    with st.spinner(f"Running Agent Pipeline for '{category_filter}'..."):
        res = st.session_state.orchestrator.run_pipeline(
            target_category="all" if category_filter == "All" else category_filter
        )
        st.sidebar.success(f"Fetched {res['raw_articles_fetched']} articles, stored {res['chunks_ingested']} chunks!")

# Knowledge Base Stats in Sidebar
stats = st.session_state.orchestrator.vector_store.get_stats()
st.sidebar.markdown("---")
st.sidebar.subheader("📊 Knowledge Base Metrics")
st.sidebar.metric("Total Vector Chunks", stats["total_chunks"])
st.sidebar.write(f"**Collection**: `{stats['collection_name']}`")
st.sidebar.write(f"**Embeddings**: `all-MiniLM-L6-v2`")

# Main Navigation Tabs
tab_chat, tab_briefing, tab_monitor = st.tabs(["💬 Interactive Chat", "☀️ Today's Briefing", "🤖 Agent Orchestrator"])

# ---------------------------------------------------------
# TAB 1: INTERACTIVE CHAT
# ---------------------------------------------------------
with tab_chat:
    st.subheader("Ask Anything About Recent News")
    st.caption("Answers are grounded strictly in collected news articles with dates and source citations.")

    # Quick sample prompt chips
    st.write("**Quick Sample Prompts:**")
    col1, col2, col3 = st.columns(3)
    sample_prompt = None
    with col1:
        if st.button("📈 What did RBI announce and market reaction?"):
            sample_prompt = "What did the RBI announce this week and how did markets react?"
    with col2:
        if st.button("🤖 What are NVIDIA and DeepMind's AI releases?"):
            sample_prompt = "What are the latest AI hardware and model releases from NVIDIA and DeepMind?"
    with col3:
        if st.button("📜 Clean Energy & EU Trade pact details?"):
            sample_prompt = "What policy decisions were made regarding Clean Energy and EU trade?"

    # User Input Field
    user_query = st.chat_input("Ask a question (e.g. 'What did the RBI announce this week and how did markets react?')")
    
    if sample_prompt:
        user_query = sample_prompt

    # Display Chat History
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "citations" in msg and msg["citations"]:
                with st.expander("📚 Verified Source Citations & Metadata"):
                    for idx, cite in enumerate(msg["citations"], 1):
                        st.markdown(
                            f"**[{idx}] {cite['headline']}**  \n"
                            f"📁 Category: `{cite.get('category', 'News')}` | 🗓️ Published: **{cite['published_date']}** | 🌐 Source: [{cite['source']}]({cite['url']})"
                        )

    if user_query:
        # Append User Message
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Generate Assistant Grounded Answer
        with st.chat_message("assistant"):
            with st.spinner("Retrieving, reranking, and generating grounded answer..."):
                start_d_str = start_date_val.strftime("%Y-%m-%d") if start_date_val else None
                result = st.session_state.query_engine.query(
                    question=user_query,
                    override_category=None if category_filter == "All" else category_filter,
                    override_start_date=start_d_str
                )

                st.markdown(result["answer"])

                if result["citations"]:
                    with st.expander("📚 Verified Source Citations & Metadata", expanded=True):
                        for idx, cite in enumerate(result["citations"], 1):
                            st.markdown(
                                f"**[{idx}] {cite['headline']}**  \n"
                                f"🗓️ Published: **{cite['published_date']}** | 🌐 Source: [{cite['source']}]({cite['url']})"
                            )

        # Append Assistant Response
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": result["answer"],
            "citations": result.get("citations", [])
        })

# ---------------------------------------------------------
# TAB 2: TODAY'S BRIEFING
# ---------------------------------------------------------
with tab_briefing:
    st.subheader(f"☀️ Executive Morning Briefing — {today.strftime('%B %d, %Y')}")
    st.caption("Auto-generated summary card partitioned by key intelligence domains.")

    if st.button("⚡ Refresh Morning Briefing"):
        st.rerun()

    briefing_data = st.session_state.query_engine.generate_daily_briefing()

    col_tech, col_fin, col_pol = st.columns(3)

    with col_tech:
        st.markdown("### 💻 Technology")
        tech_items = briefing_data.get("Tech", [])
        if tech_items:
            for item in tech_items:
                st.markdown(f"""
                <div class="briefing-card">
                    <b>{item['headline']}</b><br/>
                    <small style="color:#64748B;">{item['published_date']} | {item['source']}</small><br/>
                    <p style="margin-top:0.5rem; font-size:0.9rem;">{item['summary']}</p>
                    <a href="{item['url']}" target="_blank">Read source article →</a>
                </div>
                """, unsafe_allow_html=True)
                st.write("")
        else:
            st.info("No Tech news collected for today.")

    with col_fin:
        st.markdown("### 📊 Finance & Markets")
        fin_items = briefing_data.get("Finance", [])
        if fin_items:
            for item in fin_items:
                st.markdown(f"""
                <div class="briefing-card">
                    <b>{item['headline']}</b><br/>
                    <small style="color:#64748B;">{item['published_date']} | {item['source']}</small><br/>
                    <p style="margin-top:0.5rem; font-size:0.9rem;">{item['summary']}</p>
                    <a href="{item['url']}" target="_blank">Read source article →</a>
                </div>
                """, unsafe_allow_html=True)
                st.write("")
        else:
            st.info("No Finance news collected for today.")

    with col_pol:
        st.markdown("### 🏛️ Politics & Governance")
        pol_items = briefing_data.get("Politics", [])
        if pol_items:
            for item in pol_items:
                st.markdown(f"""
                <div class="briefing-card">
                    <b>{item['headline']}</b><br/>
                    <small style="color:#64748B;">{item['published_date']} | {item['source']}</small><br/>
                    <p style="margin-top:0.5rem; font-size:0.9rem;">{item['summary']}</p>
                    <a href="{item['url']}" target="_blank">Read source article →</a>
                </div>
                """, unsafe_allow_html=True)
                st.write("")
        else:
            st.info("No Politics news collected for today.")

# ---------------------------------------------------------
# TAB 3: AGENT ORCHESTRATOR & MONITOR
# ---------------------------------------------------------
with tab_monitor:
    st.subheader("🤖 Agent Health & Orchestration Pipeline")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success("🟢 Tech Agent: Active")
        st.caption("Feeds: TechCrunch, BBC Tech, HackerNews, Ars Technica")
    with col2:
        st.success("🟢 Finance Agent: Active")
        st.caption("Feeds: Economic Times, Moneycontrol, Business Standard, RBI")
    with col3:
        st.success("🟢 Politics Agent: Active")
        st.caption("Feeds: PIB India, Indian Express, BBC World, NYT Politics")

    st.markdown("---")
    st.subheader("📋 Pipeline Run History")
    history = st.session_state.orchestrator.get_run_history()
    if history:
        df_hist = pd.DataFrame(history)
        st.dataframe(df_hist, use_container_width=True)
    else:
        st.info("No pipeline runs executed yet.")
