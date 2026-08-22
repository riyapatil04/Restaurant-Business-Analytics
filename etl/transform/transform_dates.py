import sys
from pathlib import Path

import pandas as pd


# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def add_date_features(df: pd.DataFrame, datetime_col: str = "transaction_datetime") -> pd.DataFrame:
    """Add date/time features to a DataFrame with a datetime column."""

    df = df.copy()
    dt = df[datetime_col]

    # Basic date parts
    df["date"] = dt.dt.date
    df["year"] = dt.dt.year
    df["month"] = dt.dt.month
    df["month_name"] = dt.dt.month_name()
    df["day"] = dt.dt.day
    df["day_name"] = dt.dt.day_name()
    df["hour"] = dt.dt.hour
    df["dayofweek"] = dt.dt.dayofweek  # Monday=0, Sunday=6

    # Week number (ISO week)
    df["week"] = dt.dt.isocalendar().week

    # Quarter
    df["quarter"] = dt.dt.quarter

    # Simple weekend flag
    df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)

    return df


def main():
    # Load cleaned POS data
    pos_path = PROCESSED_DIR / "qsr_pos_cleaned.csv"
    pos = pd.read_csv(pos_path, parse_dates=["transaction_datetime", "business_day"])

    # Add date features based on transaction_datetime
    pos_enriched = add_date_features(pos, "transaction_datetime")

    print("\n" + "=" * 60)
    print("DATE TRANSFORMATION COMPLETE")
    print("=" * 60)

    print("\nOriginal columns:")
    print(pos.columns.tolist())

    print("\nNew columns added:")
    new_cols = [
        c for c in pos_enriched.columns if c not in pos.columns
    ]
    print(new_cols)

    print("\nSample rows (first 5):")
    sample_cols = [
        "order_id",
        "transaction_datetime",
        "date",
        "year",
        "month",
        "month_name",
        "day_name",
        "hour",
        "dayofweek",
        "week",
        "quarter",
        "is_weekend",
    ]
    print(pos_enriched[sample_cols].head().to_string(index=False))

    # Save enriched dataset
    output_path = PROCESSED_DIR / "qsr_pos_enriched.csv"
    pos_enriched.to_csv(output_path, index=False)

    print("\nEnriched dataset saved to:")
    print(output_path)


if __name__ == "__main__":
    main()