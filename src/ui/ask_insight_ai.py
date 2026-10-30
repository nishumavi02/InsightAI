"""
Ask InsightAI UI Component

Interactive natural-language conversational interface powering the multi-agent system.
Theme-adaptive and cleanly styled conversational decision intelligence interface.
"""

import streamlit as st
import sqlite3
from typing import List, Optional, Any

from src.ai.query_engine import process_question_with_router
from src.database.conversation_service import (
    save_conversation,
    load_conversation_history,
)
from src.ui.forecast_chart import render_forecast_chart


def render_ask_insight_ai(
    connection: sqlite3.Connection,
    chunks: Optional[List[str]] = None,
    chunk_embeddings: Optional[Any] = None,
):
    """
    Render natural-language business decision intelligence conversational interface.
    """
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = load_conversation_history(connection)

    st.markdown("### 💬 Ask InsightAI")
    st.caption("Ask natural-language questions about financial metrics, company policies, or predictive forecasts.")

    # Starter question suggestion buttons
    st.markdown("**Suggested Questions:**")
    quick_cols = st.columns(4)
    selected_quick_q = None

    with quick_cols[0]:
        if st.button("📊 Top Category Revenue", use_container_width=True):
            selected_quick_q = "Which product category generated the highest revenue?"
    with quick_cols[1]:
        if st.button("📈 3-Month Forecast", use_container_width=True):
            selected_quick_q = "Predict revenue for the next 3 months"
    with quick_cols[2]:
        if st.button("📄 Leave Policy Rules", use_container_width=True):
            selected_quick_q = "How many paid leave days does an employee receive per year?"
    with quick_cols[3]:
        if st.button("👑 VIP Customers", use_container_width=True):
            selected_quick_q = "Which customer generated the highest revenue?"

    # Question Input
    default_input = selected_quick_q or st.session_state.get("pending_user_question", "")
    user_question = st.text_input(
        "Enter your business question:",
        value=default_input,
        placeholder="e.g. Which city generated the highest sales in 2025?",
        key="ask_insightai_input",
    )

    ask_col, clear_col = st.columns([1, 5])
    with ask_col:
        submit = st.button("Ask InsightAI", type="primary", use_container_width=True)

    if (submit or selected_quick_q) and user_question.strip():
        with st.spinner("InsightAI is analyzing data across agents..."):
            response = process_question_with_router(
                question=user_question,
                connection=connection,
                chunks=chunks,
                chunk_embeddings=chunk_embeddings,
                conversation_history=st.session_state.chat_history,
            )

            # Extract fields
            if isinstance(response, dict):
                agent_name = response.get("agent", "ORCHESTRATOR")
                answer_text = response.get("answer", "")
                confidence = response.get("confidence", 0.9)
                routing_reason = response.get("routing_reason", "")
                sql_query = response.get("sql_query")
                data_df = response.get("data")
                sources = response.get("sources", [])
                forecast_meta = response.get("forecast_meta", {})
                follow_ups = response.get("follow_ups", [])
            else:
                agent_name = "ORCHESTRATOR"
                answer_text = str(response)
                confidence = 0.9
                routing_reason = "Executed query pipeline"
                sql_query = None
                data_df = None
                sources = []
                forecast_meta = {}
                follow_ups = []

            # Save to session state and database
            st.session_state.chat_history.append({
                "question": user_question,
                "answer": answer_text,
                "agent_used": agent_name,
                "confidence": confidence,
            })
            save_conversation(
                connection=connection,
                question=user_question,
                answer=answer_text,
                agent_used=agent_name,
                confidence=confidence,
            )

            # Clear pending question
            st.session_state["pending_user_question"] = ""

            # Present Active Response
            st.markdown("---")
            st.markdown("#### 🎯 Latest InsightAI Response")

            # Agent Badge & Confidence Header
            agent_badge_color = {
                "SQL": "#2563EB",
                "RAG": "#059669",
                "ML": "#D97706",
            }.get(agent_name, "#475569")

            badge_html = f"""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px; flex-wrap: wrap;">
                <span style="background-color: {agent_badge_color}; color: #FFFFFF; padding: 4px 10px; border-radius: 6px; font-weight: 600; font-size: 13px;">
                    {agent_name} Agent
                </span>
                <span style="font-size: 13px; color: var(--text-color); opacity: 0.85;">
                    Confidence: <strong>{int(confidence * 100)}%</strong> | <em>{routing_reason}</em>
                </span>
            </div>
            """
            st.markdown(badge_html, unsafe_allow_html=True)
            st.success(answer_text)

            # Detailed Agent Breakdown
            if agent_name == "SQL" and sql_query:
                with st.expander("🔍 View Executed SQL Query & Data Table", expanded=False):
                    st.code(sql_query, language="sql")
                    if data_df is not None and hasattr(data_df, "empty") and not data_df.empty:
                        st.dataframe(data_df, use_container_width=True)

            elif agent_name == "ML" and forecast_meta:
                with st.expander("📈 View Interactive Forecast Chart & Evaluation", expanded=True):
                    if data_df is not None:
                        render_forecast_chart(
                            historical_data=data_df,
                            predicted_revenue=forecast_meta.get("predicted_revenue", 0.0),
                            future_projections=forecast_meta.get("future_projections"),
                            best_model_name=forecast_meta.get("best_model_name"),
                            mae=forecast_meta.get("mae"),
                            rmse=forecast_meta.get("rmse"),
                            r2=forecast_meta.get("r2"),
                            comparison_table=forecast_meta.get("comparison_table"),
                        )
                    if forecast_meta.get("forecast_explanation"):
                        st.info(forecast_meta["forecast_explanation"])

            elif agent_name == "RAG" and sources:
                with st.expander("📄 Grounded Document Sources & Citations", expanded=True):
                    st.markdown(f"**Referenced Document:** `{', '.join(sources)}`")
                    st.caption("Answers are verified and grounded strictly in official company documents.")

            # Intelligent Suggested Follow-Ups
            if follow_ups:
                st.markdown("##### 💡 Suggested Next Questions:")
                f_cols = st.columns(len(follow_ups))
                for idx, follow_q in enumerate(follow_ups):
                    with f_cols[idx]:
                        if st.button(f"👉 {follow_q}", key=f"followup_{idx}", use_container_width=True):
                            st.session_state["pending_user_question"] = follow_q
                            st.rerun()

    # Conversation History Feed
    st.markdown("---")
    st.subheader("📜 Recent Conversation History")

    if not st.session_state.chat_history:
        st.info("No questions asked yet. Choose a suggested question above or type your own!")
    else:
        for item in reversed(st.session_state.chat_history[-10:]):
            agent_lbl = item.get("agent_used", "ORCHESTRATOR")
            conf_val = int(item.get("confidence", 0.9) * 100)
            st.markdown(
                f"""
                <div style="background-color: var(--secondary-background-color); border: 1px solid rgba(128,128,128,0.2); border-radius: 8px; padding: 14px 18px; margin-bottom: 12px;">
                    <div style="font-weight: 600; margin-bottom: 4px; color: var(--text-color);">👤 Question: {item['question']}</div>
                    <div style="margin-bottom: 6px; color: var(--text-color); opacity: 0.95;">🤖 <strong>InsightAI ({agent_lbl}):</strong> {item['answer']}</div>
                    <div style="font-size: 12px; color: var(--text-color); opacity: 0.7;">Confidence: {conf_val}% | Logged in persistent memory</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
