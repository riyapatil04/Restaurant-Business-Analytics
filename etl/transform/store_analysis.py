import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "qsr_pos_enriched.csv"

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "analytics"
OUTPUT_FILE = OUTPUT_DIR / "store_analysis.csv"


def create_store_analysis(df):

    store_analysis = (
        df.groupby("store_id")
        .agg(
            orders=("order_id", "count"),
            quantity_sold=("quantity", "sum"),
            revenue=("total_amount", "sum"),
            discount=("discount", "sum"),
            active_days=("date", "nunique")
        )
        .reset_index()
    )

    store_analysis["avg_order_value"] = (
        store_analysis["revenue"]
        / store_analysis["orders"]
    )

    store_analysis["avg_daily_revenue"] = (
        store_analysis["revenue"]
        / store_analysis["active_days"]
    )

    store_analysis["revenue_share_pct"] = (
        store_analysis["revenue"]
        / store_analysis["revenue"].sum()
        * 100
    )

    store_analysis = store_analysis.sort_values(
        "revenue",
        ascending=False
    )

    return store_analysis


def main():

    print("\n" + "=" * 60)
    print("STORE PERFORMANCE ANALYSIS")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    store_analysis = create_store_analysis(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    store_analysis.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nPOS transactions: {len(df)}")
    print(f"Stores analyzed: {len(store_analysis)}")

    print("\nStore summary:")
    print(store_analysis.to_string(index=False))

    print("\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()