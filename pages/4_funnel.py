"""
Funnel page: conversion across key lifecycle stages.
"""

import os
import sys
import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from utils.db import get_df
from utils.helpers import COLORS

st.title("🔽 User Funnel")
st.caption("Track conversion from signup to onboarding, first AI use, and power usage.")

funnel_events = get_df(
    """
    SELECT stage, COUNT(DISTINCT user_id) AS users
    FROM funnel_events
    GROUP BY stage
    """
)

stage_order = ["signed_up", "onboarded", "first_ai_use", "power_user"]
labels = {
    "signed_up": "Signed Up",
    "onboarded": "Onboarded",
    "first_ai_use": "First AI Use",
    "power_user": "Power User",
}
funnel_events["stage"] = pd.Categorical(funnel_events["stage"], categories=stage_order, ordered=True)
funnel_events = funnel_events.sort_values("stage")
funnel_events["stage_label"] = funnel_events["stage"].map(labels)

funnel_events["conversion_from_prev"] = (
    funnel_events["users"] / funnel_events["users"].shift(1).replace(0, 1) * 100
)
funnel_events["conversion_from_prev"] = funnel_events["conversion_from_prev"].fillna(100.0)

c1, c2, c3, c4 = st.columns(4)
users_list = funnel_events["users"].tolist()
c1.metric("Signups", f"{users_list[0]:,}" if len(users_list) > 0 else "0")
c2.metric("Onboarding Conversion", f"{funnel_events.iloc[1]['conversion_from_prev']:.1f}%" if len(users_list) > 1 else "0%")
c3.metric("AI Activation Conversion", f"{funnel_events.iloc[2]['conversion_from_prev']:.1f}%" if len(users_list) > 2 else "0%")
c4.metric("Power User Conversion", f"{funnel_events.iloc[3]['conversion_from_prev']:.1f}%" if len(users_list) > 3 else "0%")

fig = px.funnel(
    funnel_events,
    x="users",
    y="stage_label",
    title="AI Product Lifecycle Funnel",
    color="stage_label",
    color_discrete_sequence=COLORS["chart_sequence"],
)
st.plotly_chart(fig, use_container_width=True)

dropoff = funnel_events.copy()
dropoff["dropoff"] = dropoff["users"].shift(1) - dropoff["users"]
dropoff = dropoff.dropna()

fig_dropoff = px.bar(
    dropoff,
    x="stage_label",
    y="dropoff",
    title="Drop-Off by Stage",
    labels={"stage_label": "", "dropoff": "Users Lost"},
    color="stage_label",
    color_discrete_sequence=COLORS["chart_sequence"],
)
st.plotly_chart(fig_dropoff, use_container_width=True)

st.info(
    "PM Insight: The largest drop-off stage should drive your next experiment backlog. "
    "For AI products, activation often improves when users get value in their first session."
)
