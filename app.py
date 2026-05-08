"""
app.py - Main entry point for the ModelMetrics Dashboard.
Run with: streamlit run app.py
"""

import os
import streamlit as st

DB_PATH = os.path.join(os.path.dirname(__file__), "analytics.db")

st.set_page_config(
    page_title="ModelMetrics Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🤖 ModelMetrics Dashboard")
st.caption(
    "Portfolio project for AI Product Management: LLM performance, feature adoption, "
    "retention, and funnel analytics for a Generative AI SaaS product."
)

if not os.path.exists(DB_PATH):
    st.warning("No database found. Seed data before opening dashboard pages.")
    st.code("python data/seed_data.py")
    st.stop()

st.markdown("### Dashboard Sections")
col1, col2 = st.columns(2)
with col1:
    st.metric("📊 LLM Metrics", "Model cost, tokens, latency")
    st.metric("🚀 Feature Adoption", "Activation and repeat usage")
with col2:
    st.metric("👥 User Retention", "DAU/WAU/MAU and stickiness")
    st.metric("🔽 Funnel", "Signup to power user conversion")

st.markdown(
    """
Use the sidebar to explore each page.

This prototype uses realistic synthetic data with intentional anomalies
(like a latency incident) so you can tell a product story in interviews.
"""
)
