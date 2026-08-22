import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "qsr_pos_enriched.csv"

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "analytics"
OUTPUT_FILE = OUTPUT_DIR / "discount_analysis.csv"


def create_discount_analysis(df):

    df["discount_status"] = df["discount"].apply(
        lambda x: "Discounted" if x > 0 else "No Discount"
    )

    analysis = (
        df.groupby("discount_status")
        .agg(
            orders=("order_id", "count"),
            quantity_sold=("quantity", "sum"),
            revenue=("total_amount", "sum"),
            total_discount=("discount", "sum")
        )
        .reset_index()
    )

    analysis["avg_order_value"] = (
        analysis["revenue"] / analysis["orders"]
    )

    analysis["avg_discount_per_order"] = (
        analysis["total_discount"] / analysis["orders"]
    )

    analysis["discounted_order_share_pct"] = (
        analysis["orders"] / analysis["orders"].sum() * 100
    )

    analysis["revenue_share_pct"] = (
        analysis["revenue"] / analysis["revenue"].sum() * 100
    )

    return analysis


def main():

    print("\n" + "=" * 60)
    print("DISCOUNT ANALYSIS")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    analysis = create_discount_analysis(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    analysis.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nPOS transactions: {len(df)}")

    print("\nDiscount summary:")
    print(analysis.to_string(index=False))

    print("\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()