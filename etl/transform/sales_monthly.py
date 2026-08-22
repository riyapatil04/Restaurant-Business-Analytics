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

OUTPUT_FILE = OUTPUT_DIR / "sales_monthly.csv"


def create_monthly_sales(df):
    """Create monthly sales summary."""

    monthly_sales = (
        df.groupby(
            [
                "year",
                "month",
                "month_name"
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

    revenue_orders = (
        df.groupby(
            [
                "year",
                "month"
            ]
        )["total_amount"]
        .count()
        .reset_index(name="revenue_orders")
    )

    monthly_sales = monthly_sales.merge(
        revenue_orders,
        on=["year", "month"],
        how="left"
    )

    monthly_sales["avg_order_value"] = (
        monthly_sales["revenue"]
        / monthly_sales["revenue_orders"]
    )

    monthly_sales = monthly_sales.sort_values(
        ["year", "month"]
    )

    return monthly_sales


def main():

    print("\n" + "=" * 60)
    print("MONTHLY SALES TRANSFORMATION")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    monthly_sales = create_monthly_sales(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    monthly_sales.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nPOS transactions: {len(df)}")
    print(f"Months generated: {len(monthly_sales)}")

    print("\nMonthly summary:")
    print(
        monthly_sales.to_string(index=False)
    )

    print("\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()