"""
Generate realistic synthetic product analytics data for local demos.
Run: python data/seed_data.py
"""

import os
import random
import sqlite3
from datetime import datetime, timedelta

from faker import Faker

fake = Faker()
random.seed(42)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "analytics.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

NUM_USERS = 200
DAYS_OF_DATA = 90
AI_FEATURES = ["AI Summary", "Smart Search", "Copilot", "Auto-Tag", "Insight Generator"]
MODELS = ["gpt-4o", "gpt-3.5-turbo", "claude-3-sonnet", "claude-3-haiku"]
MODEL_COSTS = {
    "gpt-4o": 0.005,
    "gpt-3.5-turbo": 0.0005,
    "claude-3-sonnet": 0.003,
    "claude-3-haiku": 0.00025,
}


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)


def create_schema(conn: sqlite3.Connection) -> None:
    with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
        conn.executescript(schema_file.read())
    print("Schema created")


def seed_users() -> list[str]:
    return [fake.uuid4()[:8] for _ in range(NUM_USERS)]


def seed_llm_calls(conn: sqlite3.Connection, users: list[str]) -> None:
    rows = []
    start = datetime.now() - timedelta(days=DAYS_OF_DATA)
    for day_offset in range(DAYS_OF_DATA):
        current_date = start + timedelta(days=day_offset)
        is_weekday = current_date.weekday() < 5
        growth_phase = day_offset > 30
        daily_calls = random.randint(80 if is_weekday else 20, 200 if growth_phase else 120)
        for _ in range(daily_calls):
            model = random.choices(MODELS, weights=[40, 20, 30, 10])[0]
            prompt_tokens = random.randint(100, 2000)
            completion_tokens = random.randint(50, 800)
            total_tokens = prompt_tokens + completion_tokens
            cost = round((total_tokens / 1000) * MODEL_COSTS[model], 5)
            base_latency = 1800 if day_offset == 45 else random.randint(300, 2500)
            latency = base_latency + random.randint(-100, 400)
            rows.append(
                (
                    current_date.isoformat(),
                    random.choice(users),
                    random.choice(AI_FEATURES),
                    model,
                    prompt_tokens,
                    completion_tokens,
                    total_tokens,
                    cost,
                    latency,
                    1 if random.random() > 0.03 else 0,
                    random.choice([None, None, 3, 4, 4, 5, 5]),
                )
            )
    conn.executemany(
        """
        INSERT INTO llm_calls
        (timestamp, user_id, feature_name, model, prompt_tokens, completion_tokens,
         total_tokens, cost_usd, latency_ms, success, user_rating)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """,
        rows,
    )
    print(f"Seeded {len(rows)} LLM calls")


def seed_feature_events(conn: sqlite3.Connection, users: list[str]) -> None:
    rows = []
    start = datetime.now() - timedelta(days=DAYS_OF_DATA)
    for user in users:
        user_features = random.sample(AI_FEATURES, k=random.randint(1, len(AI_FEATURES)))
        for feature in user_features:
            activation_time = start + timedelta(days=random.randint(0, DAYS_OF_DATA - 1))
            rows.append((activation_time.isoformat(), user, feature, "activated", fake.uuid4()[:8]))
            for _ in range(random.randint(1, 20)):
                use_time = activation_time + timedelta(days=random.randint(1, 30))
                rows.append((use_time.isoformat(), user, feature, "used", fake.uuid4()[:8]))
    conn.executemany(
        """
        INSERT INTO feature_events (timestamp, user_id, feature_name, event_type, session_id)
        VALUES (?,?,?,?,?)
        """,
        rows,
    )
    print(f"Seeded {len(rows)} feature events")


def seed_user_activity(conn: sqlite3.Connection, users: list[str]) -> None:
    rows = []
    start = datetime.now() - timedelta(days=DAYS_OF_DATA)
    for day_offset in range(DAYS_OF_DATA):
        current_date = start + timedelta(days=day_offset)
        active_users = random.sample(users, k=int(len(users) * random.uniform(0.3, 0.55)))
        for user in active_users:
            rows.append(
                (
                    current_date.date().isoformat(),
                    user,
                    random.randint(1, 5),
                    random.randint(3, 40),
                    1 if random.random() > 0.4 else 0,
                )
            )
    conn.executemany(
        """
        INSERT INTO user_activity (date, user_id, session_count, actions_count, used_ai_feature)
        VALUES (?,?,?,?,?)
        """,
        rows,
    )
    print(f"Seeded {len(rows)} user activity rows")


def seed_funnel(conn: sqlite3.Connection, users: list[str]) -> None:
    rows = []
    start = datetime.now() - timedelta(days=DAYS_OF_DATA)
    for user in users:
        signup_time = start + timedelta(days=random.randint(0, DAYS_OF_DATA - 1))
        rows.append((signup_time.isoformat(), user, "signed_up"))
        if random.random() > 0.15:
            rows.append(((signup_time + timedelta(hours=random.randint(1, 48))).isoformat(), user, "onboarded"))
            if random.random() > 0.25:
                rows.append(((signup_time + timedelta(days=random.randint(1, 7))).isoformat(), user, "first_ai_use"))
                if random.random() > 0.5:
                    rows.append(((signup_time + timedelta(days=random.randint(14, 30))).isoformat(), user, "power_user"))
    conn.executemany(
        "INSERT INTO funnel_events (timestamp, user_id, stage) VALUES (?,?,?)",
        rows,
    )
    print(f"Seeded {len(rows)} funnel events")


def main() -> None:
    conn = get_connection()
    create_schema(conn)
    users = seed_users()
    seed_llm_calls(conn, users)
    seed_feature_events(conn, users)
    seed_user_activity(conn, users)
    seed_funnel(conn, users)
    conn.commit()
    conn.close()
    print(f"Done. Database saved at: {DB_PATH}")


if __name__ == "__main__":
    main()
