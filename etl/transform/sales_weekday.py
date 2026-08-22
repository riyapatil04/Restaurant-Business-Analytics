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

OUTPUT_FILE = OUTPUT_DIR / "sales_weekday.csv"


def create_weekday_sales(df):
    """Create weekday sales summary."""

    weekday_sales = (
        df.groupby(
            [
                "dayofweek",
                "day_name"
            ]
        )
        .agg(
            orders=("order_id", "count"),
            units_sold=("quantity", "sum"),
            revenue=("total_amount", "sum"),
            discount=("discount", "sum"),
            active_days=("date", "nunique")
        )
        .reset_index()
    )

    weekday_sales["avg_daily_revenue"] = (
        weekday_sales["revenue"]
        / weekday_sales["active_days"]
    )

    weekday_sales["avg_orders_per_day"] = (
        weekday_sales["orders"]
        / weekday_sales["active_days"]
    )

    weekday_sales["avg_order_value"] = (
        weekday_sales["revenue"]
        / weekday_sales["orders"]
    )

    weekday_sales = weekday_sales.sort_values(
        "dayofweek"
    )

    return weekday_sales


def main():

    print("\n" + "=" * 60)
    print("WEEKDAY SALES TRANSFORMATION")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    weekday_sales = create_weekday_sales(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    weekday_sales.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nPOS transactions: {len(df)}")
    print(f"Weekdays generated: {len(weekday_sales)}")

    print("\nWeekday summary:")
    print(
        weekday_sales.to_string(index=False)
    )

    print("\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()