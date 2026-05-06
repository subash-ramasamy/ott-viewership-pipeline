# OTT Viewership Pipeline

A data pipeline that ingests, cleans, and analyses OTT viewership data from 3 sources.

---

## Problem

OTT platforms and broadcasters receive viewership data from multiple sources. Each source has duplicates, missing values, and inconsistent formats. This pipeline unifies them into a single analytics-ready warehouse.

---

## Architecture

```
BARC Ratings + OTT Events + Social Feed
              ↓
     Python Cleaning Pipeline
              ↓
        Parquet Files
              ↓
       Google BigQuery
              ↓
     5 SQL Transformation Queries
```

---

## Data Sources

| Source | Raw Rows | Clean Rows | Key Issues Fixed |
|--------|----------|------------|-----------------|
| BARC TV Ratings | 315 | 293 | Duplicates, mixed dates, negative ratings, NULLs |
| OTT App Events | 5,400 | 4,955 | Duplicate events, invalid durations, anonymous users |
| Social Engagement | 1,890 | 1,785 | Invalid sentiment scores, NULL mention counts |

---

## Key Insights

| Content | Classification | Action |
|---------|---------------|--------|
| IPL 2024 Final | Star Content | Invest in live sports |
| Anupamaa S1 | Hook Fail | Review episode pacing |
| Mirzapur S3 | Hidden Gem | Increase marketing |

---

## Engineering Decisions

| Decision | Why |
|----------|-----|
| Parquet over CSV | 5x smaller, faster BigQuery loading |
| Per-show median for NULLs | Global median distorts show patterns |
| Flag anonymous users, not delete | Aggregate data still valuable |
| Deduplicate on business keys | Real duplicates have different metadata |
| WRITE_TRUNCATE in BigQuery | Prevents duplicate rows on reruns |

---

## How to Run

```bash
# Setup
git clone https://github.com/subash-ramasamy/ott-viewership-pipeline.git
cd ott-viewership-pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run pipeline
python3 scripts/generate_data.py
python3 scripts/clean_data.py
python3 scripts/load_to_bigquery.py
```

---

## Tech Stack

Python · Pandas · Parquet · BigQuery · SQL · GCP

---

## Next Steps

- Add dbt models for SQL transformations
- Add Airflow DAG for scheduling
- Build content recommendation model on top of clean data

---

## About

Built as part of my Data Engineer learning journey.
I work in media/broadcast and designed every decision
around real problems I face daily.

[LinkedIn](https://www.linkedin.com/in/subashramasamydataengineer/) · [GitHub](https://github.com/subash-ramasamy)
