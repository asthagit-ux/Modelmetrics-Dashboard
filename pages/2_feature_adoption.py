"""
Feature Adoption page: activation, usage depth, and repeat engagement.
"""

import os
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from components.charts import bar_chart, line_chart
from utils.db import get_df
from utils.helpers import COLORS, format_number

st.title("🚀 Feature Adoption")
st.caption("Understand which AI features users discover, adopt, and come back to.")

events = get_df(
    """
    SELECT DATE(timestamp) AS date, feature_name, event_type,
           COUNT(*) AS events, COUNT(DISTINCT user_id) AS users
    FROM feature_events
    GROUP BY DATE(timestamp), feature_name, event_type
    ORDER BY date
    """
)
events["date"] = pd.to_datetime(events["date"])

activated = events[events["event_type"] == "activated"]
used = events[events["event_type"] == "used"]

total_activations = int(activated["events"].sum())
total_usage = int(used["events"].sum())
adopted_features = int(activated["feature_name"].nunique())
repeat_ratio = (total_usage / total_activations) if total_activations else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Feature Activations", format_number(total_activations))
c2.metric("Feature Usage Events", format_number(total_usage))
c3.metric("Features With Adoption", format_number(adopted_features))
c4.metric("Usage / Activation", f"{repeat_ratio:.1f}x")

daily_activation = activated.groupby("date", as_index=False).agg(activations=("events", "sum"))
st.plotly_chart(
    line_chart(daily_activation, "date", "activations", "Daily AI Feature Activations", "Activations"),
    use_container_width=True,
)

left, right = st.columns(2)
with left:
    feature_adoption = activated.groupby("feature_name", as_index=False)["users"].sum().sort_values("users", ascending=False)
    st.plotly_chart(
        bar_chart(feature_adoption, "feature_name", "users", "Users Activated by Feature", "Users", "feature_name"),
        use_container_width=True,
    )

with right:
    repeat = used.groupby("feature_name", as_index=False)["events"].sum()
    repeat = repeat.merge(feature_adoption, on="feature_name", how="left")
    repeat["events_per_user"] = repeat["events"] / repeat["users"].clip(lower=1)
    fig_repeat = px.bar(
        repeat.sort_values("events_per_user", ascending=False),
        x="feature_name",
        y="events_per_user",
        title="Depth of Engagement (Uses per Activated User)",
        labels={"feature_name": "", "events_per_user": "Uses / User"},
        color="feature_name",
        color_discrete_sequence=COLORS["chart_sequence"],
    )
    st.plotly_chart(fig_repeat, use_container_width=True)

st.info(
    "PM Insight: High activation but low repeat usage usually means weak ongoing value. "
    "Focus experiments on habit loops and trigger moments after first use."
)
