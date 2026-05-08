"""
LLM Metrics page: token usage, cost, model mix, latency, and reliability.
"""

import os
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from components.charts import line_chart
from utils.db import get_df
from utils.helpers import COLORS, format_cost, format_latency, format_number

st.title("📊 LLM Metrics")
st.caption("Track token usage, cost efficiency, latency, and quality across models.")

df = get_df(
    """
    SELECT DATE(timestamp) AS date, model,
           SUM(total_tokens) AS tokens,
           SUM(cost_usd) AS cost,
           AVG(latency_ms) AS avg_latency,
           COUNT(*) AS calls,
           SUM(CASE WHEN success=0 THEN 1 ELSE 0 END) AS errors,
           AVG(CASE WHEN user_rating IS NOT NULL THEN user_rating END) AS avg_rating
    FROM llm_calls
    GROUP BY DATE(timestamp), model
    ORDER BY date
    """
)
df["date"] = pd.to_datetime(df["date"])

total_cost = df["cost"].sum()
total_tokens = df["tokens"].sum()
total_calls = df["calls"].sum()
error_rate = (df["errors"].sum() / total_calls) * 100 if total_calls else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total LLM Cost", format_cost(total_cost))
c2.metric("Total Tokens", format_number(total_tokens))
c3.metric("Avg Latency", format_latency(df["avg_latency"].mean()))
c4.metric("Error Rate", f"{error_rate:.2f}%", delta=f"{error_rate - 3:.2f}% vs 3% goal", delta_color="inverse")

daily = df.groupby("date", as_index=False).agg(cost=("cost", "sum"))
st.plotly_chart(line_chart(daily, "date", "cost", "Daily LLM Cost", "Cost (USD)"), use_container_width=True)

left, right = st.columns(2)
with left:
    model_cost = df.groupby("model", as_index=False)["cost"].sum().sort_values("cost", ascending=False)
    fig_model = px.pie(
        model_cost,
        values="cost",
        names="model",
        title="Cost Share by Model",
        color_discrete_sequence=COLORS["chart_sequence"],
    )
    st.plotly_chart(fig_model, use_container_width=True)

with right:
    model_latency = df.groupby("model", as_index=False)["avg_latency"].mean()
    fig_lat = px.bar(
        model_latency,
        x="model",
        y="avg_latency",
        title="Average Latency by Model",
        labels={"model": "", "avg_latency": "Latency (ms)"},
        color="model",
        color_discrete_sequence=COLORS["chart_sequence"],
    )
    st.plotly_chart(fig_lat, use_container_width=True)

st.info(
    "PM Insight: The most expensive model likely drives quality, but long-tail queries can be routed "
    "to lower-cost models to reduce blended cost per successful response."
)
