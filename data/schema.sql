DROP TABLE IF EXISTS llm_calls;
DROP TABLE IF EXISTS feature_events;
DROP TABLE IF EXISTS user_activity;
DROP TABLE IF EXISTS funnel_events;

CREATE TABLE llm_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    user_id TEXT NOT NULL,
    feature_name TEXT NOT NULL,
    model TEXT NOT NULL,
    prompt_tokens INTEGER NOT NULL,
    completion_tokens INTEGER NOT NULL,
    total_tokens INTEGER NOT NULL,
    cost_usd REAL NOT NULL,
    latency_ms INTEGER NOT NULL,
    success INTEGER NOT NULL,
    user_rating INTEGER
);

CREATE TABLE feature_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    user_id TEXT NOT NULL,
    feature_name TEXT NOT NULL,
    event_type TEXT NOT NULL,
    session_id TEXT NOT NULL
);

CREATE TABLE user_activity (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    user_id TEXT NOT NULL,
    session_count INTEGER NOT NULL,
    actions_count INTEGER NOT NULL,
    used_ai_feature INTEGER NOT NULL
);

CREATE TABLE funnel_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    user_id TEXT NOT NULL,
    stage TEXT NOT NULL
);
