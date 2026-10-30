"""
AI Summary Card UI Component for InsightAI
Theme-adaptive executive summary card.
"""

import streamlit as st
from typing import Dict, Any


def render_ai_summary(ai_summary: Dict[str, Any]):
    """
    Render executive AI business summary card with status badges and confidence.
    Adapts cleanly across Light, Dark, and System themes.
    """
    st.markdown("### 🤖 AI Executive Briefing")

    status = ai_summary.get("status", "Healthy")
    confidence = ai_summary.get("confidence", 95)
    reason = ai_summary.get("confidence_reason", "Verified via SQL analytics.")
    summary_text = ai_summary.get("summary", "")

    status_bg = "#10B981" if status == "Healthy" else ("#F59E0B" if status == "Stable" else "#EF4444")

    st.markdown(
        f"""
        <div style="background-color: var(--secondary-background-color); border: 1px solid rgba(128,128,128,0.2); border-left: 5px solid #2563EB; padding: 18px 22px; border-radius: 8px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
                <span style="background-color: {status_bg}; color: #FFFFFF; padding: 4px 12px; border-radius: 12px; font-size: 12px; font-weight: 600;">
                    Status: {status}
                </span>
                <span style="font-size: 13px; color: var(--text-color); opacity: 0.85;">
                    AI Verification Confidence: <strong style="color: #2563EB;">{confidence}%</strong>
                </span>
            </div>
            <p style="font-size: 15px; line-height: 1.6; margin: 0 0 10px 0; color: var(--text-color);">
                {summary_text}
            </p>
            <div style="font-size: 12px; color: var(--text-color); opacity: 0.7;">
                <em>{reason}</em>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
