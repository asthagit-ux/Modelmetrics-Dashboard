"""
Reusable Plotly chart builders to keep pages concise and consistent.
"""

import plotly.express as px

from utils.helpers import COLORS


def line_chart(df, x_col, y_col, title, y_label):
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        title=title,
        labels={x_col: "", y_col: y_label},
        color_discrete_sequence=[COLORS["primary"]],
    )
    fig.update_traces(fill="tozeroy", fillcolor="rgba(99,102,241,0.1)")
    return fig


def bar_chart(df, x_col, y_col, title, y_label, color_col=None):
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=title,
        labels={x_col: "", y_col: y_label},
        color=color_col,
        color_discrete_sequence=COLORS["chart_sequence"],
    )
    return fig
