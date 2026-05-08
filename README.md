# 🤖 ModelMetrics Dashboard

A showcase-ready portfolio project for AI Product Management roles.  
ModelMetrics Dashboard is a Streamlit app that simulates analytics for a Generative AI SaaS product and focuses on PM-relevant decisions, not vanity charts.

---

## What This Prototype Demonstrates

- LLM economics: tokens, cost, model mix, latency, reliability
- Feature adoption: activation, repeat usage, depth of engagement
- Retention: DAU/WAU/MAU trend, stickiness, AI penetration
- Funnel: signup → onboarding → first AI use → power user
- PM-style insight callouts with "so what" product framing

---

## Local Setup

### 1) Install dependencies
```bash
pip install -r requirements.txt
```

### 2) Seed realistic demo data
```bash
python data/seed_data.py
```

### 3) Launch app
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501).

---

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── .gitignore
├── data/
│   ├── schema.sql
│   └── seed_data.py
├── pages/
│   ├── 1_llm_metrics.py
│   ├── 2_feature_adoption.py
│   ├── 3_user_retention.py
│   └── 4_funnel.py
├── utils/
│   ├── db.py
│   └── helpers.py
└── components/
    └── charts.py
```

---

## GitHub + LinkedIn Showcase Tips

To make this portfolio piece stand out:

1. Add 3-5 screenshots (home + each core page)
2. Add one short demo GIF/video walkthrough
3. Pin this repo on GitHub profile
4. Share on LinkedIn with:
   - the problem statement
   - what metrics you tracked
   - one key PM insight from the dashboard
   - links to repo + live demo
