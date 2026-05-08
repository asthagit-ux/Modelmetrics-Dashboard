"""
Database access helpers for all dashboard pages.
Pages should use these helpers instead of calling sqlite3 directly.
"""

import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "analytics.db")


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def get_df(query: str, params: tuple | None = None) -> pd.DataFrame:
    conn = get_connection()
    try:
        return pd.read_sql_query(query, conn, params=params or ())
    finally:
        conn.close()
