"""
InsightAI – AI-Powered Business Decision Intelligence Platform
Streamlit Application Dashboard with Clean, Theme-Adaptive UI
"""

import sys
import sqlite3
from pathlib import Path
import streamlit as st
import pandas as pd

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import DATABASE_FILE, DOCUMENTS_DIR
from src.analytics.analytics_service import (
    get_total_revenue,
    get_total_orders,
    get_total_customers,
    get_total_products,
    get_average_customer_spending,
    get_distinct_categories,
    get_distinct_cities,
    get_date_range,
    get_key_business_facts,
    get_ai_business_highlights,
    get_top_products,
    get_top_customers,
    get_monthly_revenue_trend,
)
from src.ai.ai_service import get_ai_executive_summary
from src.ai.ml.ml_agent import run_ml_agent
from src.ai.rag.rag_agent import run_rag_agent, get_default_knowledge_base
from src.ai.rag.document_loader import load_documents_from_directory, extract_text_from_file
from src.ai.rag.document_chunker import chunk_text
from src.ai.rag.embedding_service import generate_embeddings
from src.database.conversation_service import (
    load_conversation_history,
    clear_conversation_history,
)
from src.llm.llm_service import get_configured_provider, is_llm_available

from src.ui.kpi_cards import render_kpi_cards
from src.ui.ai_summary_card import render_ai_summary
from src.ui.key_business_facts import render_key_business_facts
from src.ui.charts import (
    render_sales_analytics,
    render_revenue_trend_chart,
    render_category_revenue_chart,
    render_city_revenue_chart,
    render_customer_spending_chart,
)
from src.ui.forecast_chart import render_forecast_chart
from src.ui.ask_insight_ai import render_ask_insight_ai


# -----------------------------------------------------------------------------
# Streamlit App Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="InsightAI | Decision Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Clean, Theme-Adaptive Styling (Works in Light, Dark, and System Themes)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Metric Cards - Seamless adaptation using Streamlit theme variables */
    div[data-testid="stMetric"] {
        background-color: var(--secondary-background-color) !important;
        border: 1px solid rgba(128, 128, 128, 0.22) !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
        transition: border-color 0.15s ease, transform 0.15s ease !important;
        min-width: 0 !important;
        width: 100% !important;
        overflow: hidden !important;
    }
    
    div[data-testid="stMetric"]:hover {
        border-color: rgba(37, 99, 235, 0.5) !important;
        transform: translateY(-1px) !important;
    }
    
    div[data-testid="stMetricLabel"] {
        overflow: hidden !important;
        margin-bottom: 2px !important;
    }

    div[data-testid="stMetricLabel"] p {
        font-size: 0.76rem !important;
        font-weight: 600 !important;
        color: var(--text-color) !important;
        opacity: 0.82 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.4px !important;
        margin: 0 !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    
    /* Prevent metric value text truncation, clipping, and ellipsis */
    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] > div,
    div[data-testid="stMetricValue"] div,
    div[data-testid="stMetricValue"] span {
        overflow: visible !important;
        text-overflow: clip !important;
        white-space: nowrap !important;
        word-break: normal !important;
        width: 100% !important;
    }
    
    /* Responsive font sizing so large numbers fit cleanly without being cut off */
    div[data-testid="stMetricValue"] div {
        font-size: clamp(1.02rem, 1.22vw, 1.25rem) !important;
        font-weight: 700 !important;
        color: var(--text-color) !important;
        line-height: 1.25 !important;
        letter-spacing: -0.2px !important;
    }

    @media (max-width: 1200px) {
        div[data-testid="stMetric"] {
            padding: 8px 10px !important;
        }
        div[data-testid="stMetricValue"] div {
            font-size: clamp(0.92rem, 1.12vw, 1.15rem) !important;
        }
    }

    /* Polished Interactive Buttons */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.15s ease-in-out;
    }
    
    /* Navigation Radio Items */
    div[data-testid="stRadio"] > div {
        gap: 3px;
    }
    
    div[data-testid="stRadio"] label {
        border-radius: 6px;
        padding: 6px 10px;
        transition: background-color 0.12s ease;
    }
    
    div[data-testid="stRadio"] label:hover {
        background-color: rgba(128, 128, 128, 0.1);
    }

    /* Clean Card Container */
    .project-card {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.22);
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 16px;
    }
    
    /* Accent Line Card */
    .accent-card {
        background-color: var(--secondary-background-color);
        border: 1px solid rgba(128, 128, 128, 0.22);
        border-left: 5px solid #2563EB;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 16px;
    }
    
    /* Subtle Divider */
    hr {
        margin: 1.2rem 0;
        border-color: rgba(128, 128, 128, 0.15);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# Cached Resources & Data Loaders
# -----------------------------------------------------------------------------
@st.cache_resource
def get_db_connection():
    """Manage SQLite database connection pool."""
    conn = sqlite3.connect(DATABASE_FILE, check_same_thread=False)
    return conn


@st.cache_resource
def load_rag_knowledge_base():
    """Cache document embeddings to avoid recalculating on every user interaction."""
    return get_default_knowledge_base()


# Initialize connection and knowledge base
connection = get_db_connection()
chunks, chunk_embeddings = load_rag_knowledge_base()


# -----------------------------------------------------------------------------
# Sidebar Navigation Controls
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📊 **InsightAI**")
    st.caption("AI-Powered Decision Intelligence Platform")
    st.markdown("---")

    PAGES = [
        "1. Overview",
        "2. Business Analytics",
        "3. Ask InsightAI",
        "4. AI Executive Summary",
        "5. Revenue Forecasting",
        "6. Document Intelligence",
        "7. Conversation History",
        "8. Settings / About",
    ]

    selected_page = st.radio(
        "Navigation",
        options=PAGES,
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("#### ⚙️ System Status")
    provider_name = get_configured_provider()
    provider_badge = "🟢 " + provider_name.upper() if is_llm_available() else "🟡 OFFLINE / HEURISTIC"
    st.caption(f"**LLM Backend:** {provider_badge}")
    st.caption(f"**Database:** `insightai.db` (5,000 orders)")
    st.caption(f"**Knowledge Base:** {len(chunks)} chunks loaded")
    st.markdown("---")
    st.caption("InsightAI Decision Intelligence v2.5")


# -----------------------------------------------------------------------------
# PAGE 1: Overview
# -----------------------------------------------------------------------------
if selected_page == "1. Overview":
    st.title("📊 Executive Business Overview")
    st.caption("High-level performance summary, executive briefing, and core business metrics.")
    st.markdown("---")

    # 1. KPI Cards
    render_kpi_cards(connection)
    st.write("")

    # 2. Executive Summary Card
    ai_summary = get_ai_executive_summary(connection)
    render_ai_summary(ai_summary)

    # 3. Key Business Facts
    facts = get_key_business_facts(connection)
    render_key_business_facts(facts)

    # 4. Business Highlights
    st.markdown("### 💡 Business Highlights & Observations")
    highlights = get_ai_business_highlights(connection)
    h_col1, h_col2 = st.columns(2)
    for idx, h in enumerate(highlights):
        target_col = h_col1 if idx % 2 == 0 else h_col2
        with target_col:
            st.info(h)

    st.markdown("---")
    st.markdown("### 📈 Revenue Trajectory")
    render_revenue_trend_chart(connection)


# -----------------------------------------------------------------------------
# PAGE 2: Business Analytics
# -----------------------------------------------------------------------------
elif selected_page == "2. Business Analytics":
    st.title("📈 Business Analytics & Market Intelligence")
    st.caption("Filter and drill into multi-dimensional commercial performance.")
    st.markdown("---")

    # Interactive Filters Bar
    f_col1, f_col2, f_col3 = st.columns(3)
    categories = get_distinct_categories(connection)
    cities = get_distinct_cities(connection)
    min_date, max_date = get_date_range(connection)

    with f_col1:
        selected_category = st.selectbox("Product Category Filter", categories, index=0)
    with f_col2:
        selected_city = st.selectbox("City / Market Filter", cities, index=0)
    with f_col3:
        st.write(f"**Recorded Date Horizon:**")
        st.write(f"`{min_date}` to `{max_date}`")

    st.markdown("---")

    # Dynamic Metrics for filtered scope
    filtered_rev = get_total_revenue(connection, category=selected_category, city=selected_city)
    filtered_orders = get_total_orders(connection, category=selected_category, city=selected_city)
    filtered_avg = get_average_customer_spending(connection, category=selected_category, city=selected_city)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(f"Filtered Revenue ({selected_category})", f"Rs. {filtered_rev:,.0f}")
    with m2:
        st.metric(f"Filtered Orders", f"{filtered_orders:,}")
    with m3:
        st.metric(f"Average Customer Spending", f"Rs. {filtered_avg:,.0f}")

    st.markdown("---")

    # Visualizations
    render_sales_analytics(connection)


# -----------------------------------------------------------------------------
# PAGE 3: Ask InsightAI
# -----------------------------------------------------------------------------
elif selected_page == "3. Ask InsightAI":
    st.title("💬 Ask InsightAI – Conversational Decision Intelligence")
    st.caption("Ask natural language questions. The orchestrator routes dynamically to SQL, RAG, or ML agents.")
    st.markdown("---")

    render_ask_insight_ai(
        connection=connection,
        chunks=chunks,
        chunk_embeddings=chunk_embeddings,
    )


# -----------------------------------------------------------------------------
# PAGE 4: AI Executive Summary
# -----------------------------------------------------------------------------
elif selected_page == "4. AI Executive Summary":
    st.title("🤖 AI Executive Strategic Briefing")
    st.caption("Synthesized performance analysis, anomaly identification, and actionable commercial recommendations.")
    st.markdown("---")

    summary_data = get_ai_executive_summary(connection)
    facts = get_key_business_facts(connection)

    # Top Health Status Bar
    status = summary_data.get("status", "Healthy")
    conf = summary_data.get("confidence", 95)
    s_col1, s_col2, s_col3 = st.columns(3)
    with s_col1:
        st.metric("Overall Commercial Health", status)
    with s_col2:
        st.metric("AI Confidence Index", f"{conf}%")
    with s_col3:
        st.metric("Data Sample Scope", f"{facts['total_orders']:,} Orders")

    st.markdown("### 📋 Executive Memorandum")
    st.markdown(
        f"""
        <div style="background-color: var(--secondary-background-color); border: 1px solid rgba(128,128,128,0.22); border-left: 5px solid #2563EB; padding: 18px 22px; border-radius: 8px; margin-bottom: 24px;">
            <p style="font-size: 15px; line-height: 1.7; color: var(--text-color); margin: 0;">
                {summary_data.get('summary', '')}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🔍 Performance Diagnostic & Growth Drivers")
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        st.markdown("#### 🚀 Primary Strengths")
        st.markdown(f"- **Lead Revenue Driver:** Category `{facts['top_category']['category']}` is the commercial anchor (Rs. {facts['top_category']['total_revenue']:,.2f}).")
        st.markdown(f"- **Key Geographic Cluster:** City `{facts['top_city']['city']}` produces highest aggregate demand.")
        st.markdown(f"- **Healthy Basket Size:** Average transaction spending sits firmly at Rs. {facts['average_spending']:,.2f}.")
    with d_col2:
        st.markdown("#### ⚠️ Risks & Considerations")
        st.markdown("- **Category Concentration Risk:** Top categories account for a dominant share of total revenue; diversify product portfolio.")
        st.markdown("- **Customer Repeat Purchase Retention:** High-value customers drive significant volume, requiring loyalty incentives.")
        st.markdown("- **Supply Chain Readiness:** High-velocity categories require strict inventory buffer management.")

    st.markdown("---")
    st.markdown("### 🎯 Actionable Recommendations")
    r1, r2, r3 = st.columns(3)
    with r1:
        st.success("**1. Expand Core Categories**\n\nAllocate additional marketing budget to the top category and introduce premium SKUs.")
    with r2:
        st.warning("**2. City-Level Campaigns**\n\nScale localized logistics and promotional campaigns across emerging Tier-2 metro regions.")
    with r3:
        st.info("**3. VIP Customer Loyalty**\n\nDeploy dedicated account management and personalized discounts for top 5% spenders.")


# -----------------------------------------------------------------------------
# PAGE 5: Revenue Forecasting
# -----------------------------------------------------------------------------
elif selected_page == "5. Revenue Forecasting":
    st.title("📈 Machine Learning Revenue Forecasting")
    st.caption("Multi-model projections, model validation benchmarks, and prediction uncertainty quantification.")
    st.markdown("---")

    horizon_col, btn_col = st.columns([2, 1])
    with horizon_col:
        horizon_selection = st.selectbox(
            "Select Forecast Projection Horizon:",
            options=[1, 3, 6],
            index=1,
            format_func=lambda h: f"{h} Month{'s' if h > 1 else ''} Ahead",
        )

    # Run ML Agent
    ml_res = run_ml_agent(connection, horizon_months=horizon_selection)

    # 1. Main Forecast Visualizer
    render_forecast_chart(
        historical_data=ml_res["historical_data"],
        predicted_revenue=ml_res["predicted_revenue"],
        future_projections=ml_res["future_projections"],
        best_model_name=ml_res["best_model_name"],
        mae=ml_res["mae"],
        rmse=ml_res["rmse"],
        r2=ml_res["r2"],
        comparison_table=ml_res["comparison_table"],
    )

    # 2. Projection Schedule Table
    st.markdown("### 📅 Projected Revenue Schedule")
    proj_df = pd.DataFrame(ml_res["future_projections"])
    st.dataframe(
        proj_df.rename(columns={
            "month": "Forecast Period",
            "predicted_revenue": "Projected Revenue (Rs.)",
            "lower_bound": "Lower Bound (80% CI)",
            "upper_bound": "Upper Bound (80% CI)",
        }).style.format({
            "Projected Revenue (Rs.)": "Rs. {:,.2f}",
            "Lower Bound (80% CI)": "Rs. {:,.2f}",
            "Upper Bound (80% CI)": "Rs. {:,.2f}",
        }),
        use_container_width=True,
    )

    # 3. AI Forecast Explanation & Caveats
    st.markdown("### 🤖 Business Forecast Interpretation")
    st.info(ml_res["forecast_explanation"])
    st.caption("⚠️ **Forecasting Limitation Notice:** Statistical projections assume historical demand patterns continue. Macroeconomic shifts, competitive disruptions, or supply shocks may alter actual realizations.")


# -----------------------------------------------------------------------------
# PAGE 6: Document Intelligence
# -----------------------------------------------------------------------------
elif selected_page == "6. Document Intelligence":
    st.title("📄 Document Intelligence (RAG Knowledge Base)")
    st.caption("Ask questions about internal policies and unstructured company documents.")
    st.markdown("---")

    doc_col1, doc_col2 = st.columns([1, 2])

    with doc_col1:
        st.markdown("#### 📁 Active Documents")
        active_docs = load_documents_from_directory(DOCUMENTS_DIR)
        if active_docs:
            for d in active_docs:
                with st.expander(f"📄 {d['source']}", expanded=False):
                    st.text(d["text"][:300] + ("..." if len(d["text"]) > 300 else ""))
        else:
            st.info("No documents found in knowledge base directory.")

        st.markdown("#### 📤 Upload Document")
        uploaded_file = st.file_uploader("Upload .txt or .md file:", type=["txt", "md"])
        if uploaded_file is not None:
            save_path = DOCUMENTS_DIR / uploaded_file.name
            save_path.write_bytes(uploaded_file.getbuffer())
            st.success(f"Uploaded '{uploaded_file.name}'! Refreshing knowledge base...")
            st.cache_resource.clear()
            st.rerun()

    with doc_col2:
        st.markdown("#### 🔍 Query Knowledge Base")
        rag_query = st.text_input(
            "Enter policy question:",
            placeholder="e.g. How many days in advance must leave requests be submitted?",
        )
        if st.button("Search & Verify Document Evidence", type="primary") and rag_query.strip():
            with st.spinner("Retrieving semantic evidence..."):
                rag_res = run_rag_agent(
                    question=rag_query,
                    chunks=chunks,
                    chunk_embeddings=chunk_embeddings,
                    return_dict=True,
                )

                st.markdown("##### Grounded AI Answer")
                if rag_res.get("is_grounded", True):
                    st.success(rag_res["answer"])
                else:
                    st.warning(rag_res["answer"])

                st.markdown(f"**Retrieval Confidence:** {int(rag_res['confidence'] * 100)}%")
                if rag_res.get("evidence"):
                    st.markdown("##### 📑 Retrieved Text Passages:")
                    for idx, ev in enumerate(rag_res["evidence"]):
                        score = ev.get("score", 0.0)
                        txt = ev.get("chunk", "")
                        st.caption(f"**Passage {idx + 1}** (Similarity: {score:.3f}):")
                        st.text(txt)


# -----------------------------------------------------------------------------
# PAGE 7: Conversation History
# -----------------------------------------------------------------------------
elif selected_page == "7. Conversation History":
    st.title("📜 Persistent Conversation History")
    st.caption("Review previous queries, agent attributions, and confidence metrics stored in SQLite.")
    st.markdown("---")

    hist = load_conversation_history(connection)

    top_h1, top_h2 = st.columns([4, 1])
    with top_h1:
        st.metric("Total Stored Conversations", len(hist))
    with top_h2:
        if st.button("🗑️ Clear History", type="secondary"):
            clear_conversation_history(connection)
            if "chat_history" in st.session_state:
                st.session_state.chat_history = []
            st.success("Conversation history cleared.")
            st.rerun()

    st.markdown("---")

    if not hist:
        st.info("No recorded conversations found in the database. Questions asked via 'Ask InsightAI' will appear here.")
    else:
        # Search filter
        search_kw = st.text_input("🔍 Search Past Conversations:", placeholder="Filter by question or answer keyword...")
        filtered_hist = [h for h in hist if (search_kw.lower() in h["question"].lower() or search_kw.lower() in h["answer"].lower())] if search_kw else hist

        for turn in reversed(filtered_hist):
            agent_tag = turn.get("agent_used", "ORCHESTRATOR")
            conf_val = int(turn.get("confidence", 1.0) * 100)
            created = turn.get("created_at", "")

            st.markdown(
                f"""
                <div style="background-color: var(--secondary-background-color); border: 1px solid rgba(128,128,128,0.22); border-radius: 8px; padding: 14px 18px; margin-bottom: 12px;">
                    <div style="font-weight: 600; margin-bottom: 4px; color: var(--text-color);">👤 Question: {turn['question']}</div>
                    <div style="margin-bottom: 6px; color: var(--text-color); opacity: 0.95;">🤖 <strong>InsightAI [{agent_tag} Agent]:</strong> {turn['answer']}</div>
                    <div style="font-size: 12px; color: var(--text-color); opacity: 0.7;">Confidence: {conf_val}% | Logged at: {created}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Export table
        st.markdown("#### 📥 Export History Transcript")
        hist_df = pd.DataFrame(hist)
        st.download_button(
            "Download Transcript (CSV)",
            data=hist_df.to_csv(index=False),
            file_name="insightai_conversation_history.csv",
            mime="text/csv",
        )


# -----------------------------------------------------------------------------
# PAGE 8: Settings / About
# -----------------------------------------------------------------------------
elif selected_page == "8. Settings / About":
    st.title("⚙️ System Configuration & Platform Overview")
    st.caption("InsightAI operational parameters, environment settings, and architecture specifications.")
    st.markdown("---")

    col_s1, col_s2 = st.columns(2)

    with col_s1:
        st.markdown("### 🔌 Active AI Providers")
        provider = get_configured_provider()
        st.write(f"**Configured Provider:** `{provider.upper()}`")
        st.write(f"**LLM Connected:** `{'Yes' if is_llm_available() else 'No (Offline Fallback Engine Active)'}`")
        st.write(f"**Database Engine:** `SQLite 3`")
        st.write(f"**Database Location:** `{DATABASE_FILE}`")
        st.write(f"**Vector Engine:** `Sentence-Transformers / Scikit-Learn Hybrid`")

        st.markdown("---")
        st.markdown("### 💾 Database Maintenance")
        if st.button("🔄 Verify Database Connection"):
            cur = connection.cursor()
            cur.execute("SELECT COUNT(*) FROM orders")
            cnt = cur.fetchone()[0]
            st.success(f"Connection OK! Found {cnt:,} orders in database.")

    with col_s2:
        st.markdown("### 🏛️ System Architecture")
        st.markdown(
            """
            ```
            User Question
                 │
                 ▼
            LLM Decision Router (Context-Aware)
                 │
                 ├──► SQL Agent (Natural Language -> SQL -> Safe Execution)
                 ├──► RAG Agent (Document Retrieval -> Context Grounding)
                 └──► ML Agent  (Multi-Model Revenue Forecasting)
                 │
                 ▼
            Agent Orchestrator
                 │
                 ▼
            AI Reasoning Layer (Follow-ups & Confidence)
                 │
                 ▼
            Synthesized Final Response
            ```
            """
        )

    st.markdown("---")
    st.markdown("### 🏢 Platform Specifications & Technical Capabilities")
    st.markdown(
        """
        * **Platform Name:** InsightAI – AI-Powered Business Decision Intelligence Platform
        * **Core Purpose:** Deliver self-service commercial intelligence by bridging relational databases,
          unstructured knowledge bases, and predictive ML forecasting through natural language.
        * **Core Technical Capabilities:**
          * **Intelligent Routing:** Context-aware intent classification dynamically delegating queries across specialized SQL, RAG, and ML agents.
          * **Database Intelligence:** Natural-Language-to-SQL query generation, strict read-only safety validation, and automated error recovery.
          * **Document Intelligence:** Retrieval-Augmented Generation (RAG) with dual-engine vectorization and strict confidence thresholding to prevent hallucinations.
          * **Predictive Analytics:** Multi-model revenue forecasting comparing Linear Regression, Ridge, and Random Forest algorithms with automated MAE, RMSE, and $R^2$ evaluation.
          * **Enterprise UI:** Adaptive interface engineered for high contrast and accessibility across Light, Dark, and System display modes.
        """
    )
