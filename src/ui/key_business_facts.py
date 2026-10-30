"""
Key Business Facts UI Component for InsightAI
"""

import streamlit as st
from typing import Dict, Any


def render_key_business_facts(facts: Dict[str, Any]):
    """
    Render key business facts cards.
    """
    st.markdown("### 📌 Key Business Facts")

    fact1, fact2, fact3, fact4 = st.columns(4)

    with fact1:
        top_cat = facts.get("top_category", {})
        st.metric(
            "🏆 Top Category",
            top_cat.get("category", "N/A"),
            help=f"Revenue: Rs. {top_cat.get('total_revenue', 0):,.2f}",
        )

    with fact2:
        top_city = facts.get("top_city", {})
        st.metric(
            "🏙️ Top City",
            top_city.get("city", "N/A"),
            help=f"Revenue: Rs. {top_city.get('total_revenue', 0):,.2f}",
        )

    with fact3:
        top_cust = facts.get("top_customer", {})
        st.metric(
            "👑 Top Customer",
            top_cust.get("customer_name", "N/A"),
            help=f"Total Spent: Rs. {top_cust.get('total_spent', 0):,.2f}",
        )

    with fact4:
        total_rev = facts.get("total_revenue", 0.0)
        st.metric(
            "💰 Recorded Revenue",
            f"Rs. {total_rev:,.0f}",
        )
