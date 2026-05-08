"""
User Retention page: DAU/WAU/MAU and AI usage stickiness trends.
"""

import os
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from components.charts import line_chart
from utils.db import get_df

st.title("👥 User Retention")
st.caption("Measure active user trends and stickiness for the AI product experience.")

activity = get_df(
    """
    SELECT date, user_id, used_ai_feature
    FROM user_activity
    ORDER BY date
    """
)
activity["date"] = pd.to_datetime(activity["date"])

dau = activity.groupby("date", as_index=False)["user_id"].nunique().rename(columns={"user_id": "dau"})
daily_ai_users = activity[activity["used_ai_feature"] == 1].groupby("date", as_index=False)["user_id"].nunique()
daily_ai_users = daily_ai_users.rename(columns={"user_id": "ai_users"})

dau = dau.merge(daily_ai_users, on="date", how="left").fillna({"ai_users": 0})
dau["wau"] = dau["dau"].rolling(7, min_periods=1).mean()
dau["mau"] = dau["dau"].rolling(30, min_periods=1).mean()
dau["stickiness"] = (dau["dau"] / dau["mau"].replace(0, 1)) * 100
dau["ai_penetration"] = (dau["ai_users"] / dau["dau"].replace(0, 1)) * 100

c1, c2, c3, c4 = st.columns(4)
c1.metric("Latest DAU", f"{int(dau.iloc[-1]['dau']):,}")
c2.metric("7-Day Avg (WAU Proxy)", f"{dau.iloc[-1]['wau']:.0f}")
c3.metric("30-Day Avg (MAU Proxy)", f"{dau.iloc[-1]['mau']:.0f}")
c4.metric("DAU/MAU Stickiness", f"{dau.iloc[-1]['stickiness']:.1f}%")

left, right = st.columns(2)
with left:
    st.plotly_chart(line_chart(dau, "date", "dau", "Daily Active Users", "Users"), use_container_width=True)
with right:
    fig_sticky = px.line(
        dau,
        x="date",
        y="stickiness",
        title="DAU/MAU Stickiness Trend",
        labels={"date": "", "stickiness": "Stickiness (%)"},
    )
    st.plotly_chart(fig_sticky, use_container_width=True)

fig_ai = px.area(
    dau,
    x="date",
    y="ai_penetration",
    title="AI Feature Penetration Among Active Users",
    labels={"date": "", "ai_penetration": "AI Penetration (%)"},
    color_discrete_sequence=["#22C55E"],
)
st.plotly_chart(fig_ai, use_container_width=True)

st.info(
    "PM Insight: If stickiness rises while AI penetration also rises, your AI features are likely "
    "driving retention rather than acting as one-off novelty tools."
)
