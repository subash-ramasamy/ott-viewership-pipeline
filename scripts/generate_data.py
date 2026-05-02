import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

np.random.seed(42) #controls numpy random
random.seed(42) #controls python random

SHOWS = [
    ("Anupama", "Star Plus", "Drama", "Hindi"),
    ("Big Boss", "Colors TV", "Reality Show", "Hindi"),
    ("KBC", "Sony LIV", "Reality Show", "Hindi"),
    ("Tarak Mehta", "Sony LIV", "Comedy", "Hindi"),
    ("Nayagi", "SUN TV", "Drama", "Tamil"),
]

CITIES = ["Mumbai", "Delhi", "Chennai", "Bangalore", "Hyderabad"]

CITY_TIERS = {
    "Mumbai" : "Tier 1",
    "Delhi" : "Tier 1",
    "Chennai" : "Tier 1",
    "Bangalore" : "Tier 1",
    "Hyderabad" : "Tier 2",
}

DEVICES = ["Mobile", "Smart TV", "Tablet", "Laptop"]

SUBSCRIPTIONS = [ "Free", "Basic", "Premium", "Annual"]

CONTENT_CATALOG = [
    ("C001", "Anupamaa S1",        "Series",   45),
    ("C002", "KBC Season 15",      "GameShow", 60),
    ("C003", "IPL 2024 Final",     "Sports",  210),
    ("C004", "Panchayat S3",       "Series",   30),
    ("C005", "Mirzapur S3",        "Thriller", 55),
]

PLATFORMS = ["Twitter", "Instagram", "YouTube", "Facebook"]

def generate_barc_ratings(n_weeks):
    print(f"Generating BARC ratings for {n_weeks} weeks...")
    records = []

    for week in range(1,n_weeks + 1):
        air_date = datetime(2024,1,1) + timedelta(weeks=week)
        for show_name, channel, genre, language in SHOWS:
            for city in CITIES:
                tier = CITY_TIERS[city]

                base_rating = (
                    random.uniform(0.5, 8.0) if tier == "Tier 1"
                    else random.uniform(0.1,4.0)
                               )
                record = {
                    "show_id" : f"SH_{SHOWS.index((show_name, channel, genre, language))+1:03d}",
                    "show_name":       show_name,
                    "channel":         channel,
                    "genre":           genre,
                    "language":        language,
                    "air_date":        air_date.strftime("%Y-%m-%d"),
                    "city":            city,
                    "city_tier":       tier,
                    "ratings_million": round(base_rating, 2),
                    "week_number":     week,
                    "source":          "BARC"
                }
                records.append(record)
    df = pd.DataFrame(records)
      
    # Inject Messiness
    print("Injecting Messiness...")

    dupes = df.sample(frac =0.05, random_state = 1)
    df =pd.concat([df,dupes], ignore_index=True)

    null_idx = df.sample(frac=0.08, random_state = 2).index
    df.loc[null_idx,"ratings_million"] = np.nan

    neg_idx = df.sample(n=10, random_state = 4).index
    df.loc[neg_idx, "ratings_million"] = -1.0

    fmt_idx = df.sample(frac=0.10, random_state=3).index
    df.loc[fmt_idx, "air_date"] = pd.to_datetime(
    df.loc[fmt_idx, "air_date"],
    errors="coerce"
    ).dt.strftime("%d/%m/%Y")

    print(f"BARC done: {len(df):,} rows")
    return df

def generate_ott_events(n_events):
    print("Generating OTT events...")
    records = []
    user_ids = [f"U{str(i).zfill(5)}" for i in range(1, 501)]

    for i in range(n_events):
        cid, cname, ctype, total = random.choice(CONTENT_CATALOG)
        completion = random.choices(
            [0.25, 0.5, 0.75, 1.0],
            weights=[20, 30, 25, 25]
        )[0]
        city = random.choice(CITIES)
        ts   = datetime(2024, 1, 1) + timedelta(
            days=random.randint(0, 90),
            hours=random.randint(6, 23)
        )
        records.append({
            "event_id":            f"EVT_{i+1:06d}",
            "user_id":             random.choice(user_ids),
            "content_id":          cid,
            "content_name":        cname,
            "content_type":        ctype,
            "watch_duration_mins": round(total * completion, 1),
            "total_duration_mins": total,
            "completion_pct":      round(completion * 100, 1),
            "device_type":         random.choice(DEVICES),
            "subscription_tier":   random.choice(SUBSCRIPTIONS),
            "city":                city,
            "city_tier":           CITY_TIERS[city],
            "event_timestamp":     ts.strftime("%Y-%m-%d %H:%M:%S"),
            "source":              "OTT_APP"
        })

    df = pd.DataFrame(records)

    # Inject messiness
    print("Injecting Messiness...")

    dupes     = df.sample(frac=0.08, random_state=10)
    df        = pd.concat([df, dupes], ignore_index=True)

    null_idx  = df.sample(frac=0.05, random_state=11).index
    df.loc[null_idx, "user_id"] = np.nan

    bug_idx   = df.sample(n=50, random_state=12).index
    df.loc[bug_idx, "watch_duration_mins"] = (
        df.loc[bug_idx, "total_duration_mins"] * 2
    )

    ts_idx = df.sample(frac=0.10, random_state=13).index
    df.loc[ts_idx, "event_timestamp"] = (
    df.loc[ts_idx, "event_timestamp"]
    .str.replace(" ", "T") + "Z"
    )

    print(f"OTT done: {len(df):,} rows")
    return df


def generate_social_feed(n_days):
    print("Generating social feed...")
    records = []

    for day in range(n_days):
        date = datetime(2024, 1, 1) + timedelta(days=day)
        for idx, (cid, cname, _, _) in enumerate(CONTENT_CATALOG):
            for platform in PLATFORMS:
                records.append({
                    "content_id":      cid,
                    "content_name":    cname,
                    "platform":        platform,
                    "mention_count":   random.randint(100, 50000),
                    "sentiment_score": round(random.uniform(-1.0, 1.0), 3),
                    "trending_rank":   random.randint(1, 50),
                    "recorded_date":   date.strftime("%Y-%m-%d"),
                    "source":          "SOCIAL"
                })

    df = pd.DataFrame(records)

   # Inject messiness
    print("Injecting Messiness...")

    bad_idx  = df.sample(n=20, random_state=20).index
    df.loc[bad_idx, "sentiment_score"] = 99.0

    null_idx = df.sample(frac=0.06, random_state=21).index
    df.loc[null_idx, "mention_count"]  = np.nan

    print(f"Social done: {len(df):,} rows")
    return df


def main():
    os.makedirs("data/raw", exist_ok=True)

    barc   = generate_barc_ratings(n_weeks=12)
    ott    = generate_ott_events(n_events=5000)
    social = generate_social_feed(n_days=90)

    barc.to_csv("data/raw/barc_ratings_raw.csv",       index=False)
    ott.to_csv("data/raw/ott_events_raw.csv",           index=False)
    social.to_csv("data/raw/social_engagement_raw.csv", index=False)

    print(f"BARC:   {len(barc):,} rows")
    print(f"OTT:    {len(ott):,} rows")
    print(f"Social: {len(social):,} rows")
    print("All saved to data/raw/")


if __name__ == "__main__":
    main()