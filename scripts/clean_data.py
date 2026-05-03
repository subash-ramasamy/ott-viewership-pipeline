import pandas as pd
import numpy as np
import logging
import os
from datetime import datetime

# Logging Setup
os.makedirs("logs",exist_ok = True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def standardise_date(date_str):
    if pd.isna(date_str):
        return None
    for fmt in ["%Y-%m-%d", "%d/%m/%Y"]:
        try:
            return datetime.strptime(
                str(date_str), fmt
            ).strftime("%Y-%m-%d")
        except ValueError:
            continue
    logger.warning(f"Could not parse date: {date_str}")
    return None

def clean_barc(filepath):
    logger.info("Cleaning BARC data...")

    df       = pd.read_csv(filepath)
    raw_rows = len(df)
    logger.info(f"Loaded {raw_rows:,} raw rows")

    # 1. Remove duplicates
    df = df.drop_duplicates()
    logger.info(f"Removed {raw_rows - len(df)} duplicates")

    # 2. Fix date formats
    df["air_date"] = df["air_date"].apply(standardise_date)

    # 3. Fix show name casing
    df["show_name"] = df["show_name"].str.title().str.strip()

    # 4. Remove negative ratings
    invalid = df["ratings_million"] < 0
    logger.warning(f"Removing {invalid.sum()} negative ratings")
    df = df[~invalid]

    # 5. Fill NULL ratings with show median
    median = df.groupby("show_name")["ratings_million"].transform("median")
    nulls  = df["ratings_million"].isna().sum()
    df["ratings_million"] = df["ratings_million"].fillna(median)
    logger.info(f"Filled {nulls} NULL ratings with show median")

    logger.info(f"BARC cleaned: {len(df):,} rows")
    return df

def clean_ott(filepath):
    logger.info("Cleaning OTT data...")

    df       = pd.read_csv(filepath)
    raw_rows = len(df)
    logger.info(f"Loaded {raw_rows:,} raw rows")

    # 1. Deduplicate on event_id
    df = df.drop_duplicates(subset=["event_id"])
    logger.info(f"Removed {raw_rows - len(df)} duplicate events")

    # 2. Remove invalid watch durations
    invalid = df["watch_duration_mins"] > df["total_duration_mins"] * 1.05
    logger.warning(f"Removing {invalid.sum()} invalid watch durations")
    df = df[~invalid]

    # 3. Flag anonymous users — don't delete them
    df["is_anonymous"] = df["user_id"].isna()
    df["user_id"]      = df["user_id"].fillna("ANONYMOUS")
    logger.info(f"Flagged {df['is_anonymous'].sum()} anonymous users")

    # 4. Recalculate completion percentage
    df["completion_pct"] = (
        df["watch_duration_mins"] /
        df["total_duration_mins"] * 100
    ).round(1).clip(0, 100)

    logger.info(f"OTT cleaned: {len(df):,} rows")
    return df

def clean_social(filepath):
    logger.info("Cleaning Social data...")

    df = pd.read_csv(filepath)
    raw_rows = len(df)
    logger.info(f"Loaded {raw_rows:,} raw rows")

    # 1. Remove invalid sentiment scores
    invalid = (df["sentiment_score"] < -1) | (df["sentiment_score"] > 1)
    logger.warning(f"Removing {invalid.sum()} invalid sentiment rows")
    df = df[~invalid]

    # 2. Fill NULL mention counts with 0
    df["mention_count"] = df["mention_count"].fillna(0).astype(int)

    # 3. Deduplicate
    df = df.drop_duplicates(subset=["content_id", "platform", "recorded_date"])
    logger.info(f"Removed {raw_rows - len(df)} duplicate events")

    logger.info(f"Social cleaned: {len(df):,} rows")
    return df

def save_parquet(df, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path, index=False)
    size = os.path.getsize(path) / 1024
    logger.info(f"Saved {len(df):,} rows → {path} ({size:.1f} KB)")


def main():
    logger.info("Cleaning Pipeline Started")

    barc   = clean_barc("data/raw/barc_ratings_raw.csv")
    ott    = clean_ott("data/raw/ott_events_raw.csv")
    social = clean_social("data/raw/social_engagement_raw.csv")

    save_parquet(barc,   "data/parquet/barc_clean.parquet")
    save_parquet(ott,    "data/parquet/ott_clean.parquet")
    save_parquet(social, "data/parquet/social_clean.parquet")

    logger.info("Pipeline Complete")
    logger.info(f"BARC:   {len(barc):,} rows")
    logger.info(f"OTT:    {len(ott):,} rows")
    logger.info(f"Social: {len(social):,} rows")



if __name__ == "__main__":
    main()
