import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))


INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "qsr_pos_enriched.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "analytics"
)

OUTPUT_FILE = OUTPUT_DIR / "sales_daily.csv"


def create_daily_sales(df):
    """Create daily sales summary."""

    daily_sales = (
        df.groupby(
            [
                "date",
                "day_name",
                "dayofweek",
                "is_weekend"
            ]
        )
        .agg(
            orders=("order_id", "count"),
            units_sold=("quantity", "sum"),
            revenue=("total_amount", "sum"),
            discount=("discount", "sum")
        )
        .reset_index()
    )

    # Calculate average order value using transactions
    # that have a recorded total amount.
    revenue_orders = (
        df.groupby("date")["total_amount"]
        .count()
        .reset_index(name="revenue_orders")
    )

    daily_sales = daily_sales.merge(
        revenue_orders,
        on="date",
        how="left"
    )

    daily_sales["avg_order_value"] = (
        daily_sales["revenue"]
        / daily_sales["revenue_orders"]
    )

    return daily_sales


def main():

    print("\n" + "=" * 60)
    print("DAILY SALES TRANSFORMATION")
    print("=" * 60)

    # Load enriched POS data
    df = pd.read_csv(INPUT_FILE)

    # Convert date back to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Create daily summary
    daily_sales = create_daily_sales(df)

    # Create output directory
    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save result
    daily_sales.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nPOS transactions: {len(df)}")
    print(f"Days generated: {len(daily_sales)}")

    print("\nColumns:")
    print(list(daily_sales.columns))

    print("\nSample:")
    print(
        daily_sales
        .head(10)
        .to_string(index=False)
    )

    print("\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()