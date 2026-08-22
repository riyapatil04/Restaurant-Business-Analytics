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


def analyze_dimension(df, column):

    result = (
        df.groupby(column)
        .agg(
            orders=("order_id", "count"),
            quantity_sold=("quantity", "sum"),
            revenue=("total_amount", "sum"),
            discount=("discount", "sum")
        )
        .reset_index()
    )

    result["avg_order_value"] = (
        result["revenue"] / result["orders"]
    )

    result["revenue_share_pct"] = (
        result["revenue"]
        / result["revenue"].sum()
        * 100
    )

    result = result.sort_values(
        "revenue",
        ascending=False
    )

    return result


def create_operations_analysis(df):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Hour analysis
    hourly = analyze_dimension(df, "hour")
    hourly.to_csv(
        OUTPUT_DIR / "operations_hourly.csv",
        index=False
    )

    # Daypart analysis
    daypart = analyze_dimension(df, "daypart")
    daypart.to_csv(
        OUTPUT_DIR / "operations_daypart.csv",
        index=False
    )

    # Weekday analysis
    weekday = analyze_dimension(df, "day_name")
    weekday.to_csv(
        OUTPUT_DIR / "operations_weekday.csv",
        index=False
    )

    return hourly, daypart, weekday


def main():

    print("\n" + "=" * 60)
    print("OPERATIONS & PEAK PERIOD ANALYSIS")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    hourly, daypart, weekday = create_operations_analysis(df)

    print(f"\nPOS transactions: {len(df)}")

    print("\n--- PEAK HOURS ---")
    print(
        hourly.head(10).to_string(index=False)
    )

    print("\n--- DAYPART PERFORMANCE ---")
    print(
        daypart.to_string(index=False)
    )

    print("\n--- WEEKDAY PERFORMANCE ---")
    print(
        weekday.to_string(index=False)
    )

    peak_hour = hourly.iloc[0]
    peak_daypart = daypart.iloc[0]
    peak_weekday = weekday.iloc[0]

    print("\n--- PEAK PERIODS ---")

    print(
        f"Highest revenue hour: "
        f"{peak_hour['hour']}:00 "
        f"({peak_hour['revenue']:.2f})"
    )

    print(
        f"Highest revenue daypart: "
        f"{peak_daypart['daypart']} "
        f"({peak_daypart['revenue']:.2f})"
    )

    print(
        f"Highest revenue weekday: "
        f"{peak_weekday['day_name']} "
        f"({peak_weekday['revenue']:.2f})"
    )

    print("\nSaved files:")
    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()