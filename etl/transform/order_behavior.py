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

OUTPUT_FILE = OUTPUT_DIR / "order_behavior.csv"


def create_order_behavior(df):

    # Each row represents an order/item transaction.
    # Group by order_id to understand the complete order.
    orders = (
        df.groupby("order_id")
        .agg(
            date=("date", "first"),
            day_name=("day_name", "first"),
            hour=("hour", "first"),
            daypart=("daypart", "first"),
            service_mode=("service_mode", "first"),
            payment_type=("payment_type", "first"),
            items=("quantity", "sum"),
            order_revenue=("total_amount", "sum"),
            discount=("discount", "sum")
        )
        .reset_index()
    )

    # Classify order size
    orders["order_size"] = pd.cut(
        orders["items"],
        bins=[0, 1, 2, 3, float("inf")],
        labels=[
            "1 Item",
            "2 Items",
            "3 Items",
            "4+ Items"
        ]
    )

    # Hourly performance
    hourly = (
        orders.groupby("hour", observed=False)
        .agg(
            orders=("order_id", "count"),
            items_sold=("items", "sum"),
            revenue=("order_revenue", "sum"),
            avg_order_value=("order_revenue", "mean")
        )
        .reset_index()
    )

    hourly["revenue_share_pct"] = (
        hourly["revenue"]
        / hourly["revenue"].sum()
        * 100
    )

    # Order-size performance
    size_analysis = (
        orders.groupby("order_size", observed=False)
        .agg(
            orders=("order_id", "count"),
            items_sold=("items", "sum"),
            revenue=("order_revenue", "sum"),
            avg_order_value=("order_revenue", "mean")
        )
        .reset_index()
    )

    size_analysis["order_share_pct"] = (
        size_analysis["orders"]
        / size_analysis["orders"].sum()
        * 100
    )

    # Save the detailed order-level data
    orders_file = OUTPUT_DIR / "orders_behavior_detail.csv"

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    orders.to_csv(
        orders_file,
        index=False
    )

    # Save hourly analysis
    hourly_file = OUTPUT_DIR / "order_behavior_hourly.csv"

    hourly.to_csv(
        hourly_file,
        index=False
    )

    # Save order-size analysis
    size_file = OUTPUT_DIR / "order_size_analysis.csv"

    size_analysis.to_csv(
        size_file,
        index=False
    )

    return orders, hourly, size_analysis


def main():

    print("\n" + "=" * 60)
    print("ORDER BEHAVIOR ANALYSIS")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    orders, hourly, size_analysis = create_order_behavior(df)

    print(f"\nPOS transaction rows: {len(df)}")
    print(f"Unique orders: {len(orders)}")

    print("\nOverall order behavior:")

    print(
        f"Average items per order: "
        f"{orders['items'].mean():.2f}"
    )

    print(
        f"Average order value: "
        f"{orders['order_revenue'].mean():.2f}"
    )

    print(
        f"Largest order: "
        f"{orders['items'].max()} items"
    )

    print("\nHourly performance:")
    print(hourly.to_string(index=False))

    print("\nOrder-size analysis:")
    print(size_analysis.to_string(index=False))

    print("\nSaved files:")
    print(
        PROJECT_ROOT
        / "data"
        / "processed"
        / "analytics"
    )


if __name__ == "__main__":
    main()