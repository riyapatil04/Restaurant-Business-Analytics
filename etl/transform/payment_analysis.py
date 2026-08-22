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

OUTPUT_FILE = OUTPUT_DIR / "payment_analysis.csv"


def create_payment_analysis(df):
    """Create payment-method performance analysis."""

    payment_analysis = (
        df.groupby("payment_type")
        .agg(
            orders=("order_id", "count"),
            quantity_sold=("quantity", "sum"),
            revenue=("total_amount", "sum"),
            discount=("discount", "sum")
        )
        .reset_index()
    )

    payment_analysis["avg_order_value"] = (
        payment_analysis["revenue"]
        / payment_analysis["orders"]
    )

    payment_analysis["revenue_share_pct"] = (
        payment_analysis["revenue"]
        / payment_analysis["revenue"].sum()
        * 100
    )

    payment_analysis = payment_analysis.sort_values(
        "revenue",
        ascending=False
    )

    return payment_analysis


def main():

    print("\n" + "=" * 60)
    print("PAYMENT METHOD ANALYSIS")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    payment_analysis = create_payment_analysis(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    payment_analysis.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nPOS transactions: {len(df)}")
    print(
        f"Payment types analyzed: "
        f"{len(payment_analysis)}"
    )

    print("\nPayment summary:")

    print(
        payment_analysis.to_string(index=False)
    )

    print("\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()