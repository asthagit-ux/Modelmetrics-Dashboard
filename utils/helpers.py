"""
Shared constants and formatting helpers used across dashboard pages.
Keeping this centralized ensures consistent visuals and metric formatting.
"""

COLORS = {
    "primary": "#6366F1",
    "secondary": "#22C55E",
    "accent": "#F59E0B",
    "danger": "#EF4444",
    "muted": "#94A3B8",
    "chart_sequence": ["#6366F1", "#22C55E", "#F59E0B", "#EC4899", "#14B8A6", "#8B5CF6"],
}


def format_cost(value: float) -> str:
    return f"${value:,.2f}"


def format_number(value: float) -> str:
    return f"{int(value):,}"


def format_latency(ms: float) -> str:
    return f"{int(ms):,} ms"
