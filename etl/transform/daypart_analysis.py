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

OUTPUT_FILE = OUTPUT_DIR / "daypart_analysis.csv"


def create_daypart_analysis(df):
    """Create daypart sales and performance analysis."""

    daypart_analysis = (
        df.groupby("daypart")
        .agg(
            orders=("order_id", "count"),
            quantity_sold=("quantity", "sum"),
            revenue=("total_amount", "sum"),
            discount=("discount", "sum"),
            active_days=("date", "nunique")
        )
        .reset_index()
    )

    daypart_analysis["avg_order_value"] = (
        daypart_analysis["revenue"]
        / daypart_analysis["orders"]
    )

    daypart_analysis["avg_daily_revenue"] = (
        daypart_analysis["revenue"]
        / daypart_analysis["active_days"]
    )

    daypart_analysis["revenue_share_pct"] = (
        daypart_analysis["revenue"]
        / daypart_analysis["revenue"].sum()
        * 100
    )

    return daypart_analysis


def main():

    print("\n" + "=" * 60)
    print("DAYPART ANALYSIS")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    daypart_analysis = create_daypart_analysis(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    daypart_analysis.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nPOS transactions: {len(df)}")
    print(
        f"Dayparts analyzed: "
        f"{len(daypart_analysis)}"
    )

    print("\nDaypart summary:")

    print(
        daypart_analysis.to_string(index=False)
    )

    print("\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()