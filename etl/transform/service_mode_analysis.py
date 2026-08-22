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

OUTPUT_FILE = OUTPUT_DIR / "service_mode_analysis.csv"


def create_service_mode_analysis(df):
    """Create service-channel performance analysis."""

    service_analysis = (
        df.groupby("service_mode")
        .agg(
            orders=("order_id", "count"),
            quantity_sold=("quantity", "sum"),
            revenue=("total_amount", "sum"),
            discount=("discount", "sum"),
            active_days=("date", "nunique")
        )
        .reset_index()
    )

    service_analysis["avg_order_value"] = (
        service_analysis["revenue"]
        / service_analysis["orders"]
    )

    service_analysis["avg_daily_revenue"] = (
        service_analysis["revenue"]
        / service_analysis["active_days"]
    )

    service_analysis["revenue_share_pct"] = (
        service_analysis["revenue"]
        / service_analysis["revenue"].sum()
        * 100
    )

    service_analysis = service_analysis.sort_values(
        "revenue",
        ascending=False
    )

    return service_analysis


def main():

    print("\n" + "=" * 60)
    print("SERVICE MODE ANALYSIS")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    service_analysis = create_service_mode_analysis(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    service_analysis.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nPOS transactions: {len(df)}")
    print(
        f"Service modes analyzed: "
        f"{len(service_analysis)}"
    )

    print("\nService mode summary:")

    print(
        service_analysis.to_string(index=False)
    )

    print("\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()