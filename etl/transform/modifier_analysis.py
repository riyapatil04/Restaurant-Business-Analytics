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

OUTPUT_FILE = OUTPUT_DIR / "modifier_analysis.csv"


def create_modifier_analysis(df):

    # Replace missing modifiers with a meaningful label.
    df["modifier_clean"] = df["modifier"].fillna("No Modifier")

    analysis = (
        df.groupby("modifier_clean")
        .agg(
            orders=("order_id", "count"),
            quantity_sold=("quantity", "sum"),
            revenue=("total_amount", "sum"),
            discount=("discount", "sum")
        )
        .reset_index()
    )

    # Average revenue generated per transaction
    analysis["avg_order_value"] = (
        analysis["revenue"]
        / analysis["orders"]
    )

    # Percentage of transactions using the modifier
    analysis["usage_share_pct"] = (
        analysis["orders"]
        / analysis["orders"].sum()
        * 100
    )

    # Revenue contribution
    analysis["revenue_share_pct"] = (
        analysis["revenue"]
        / analysis["revenue"].sum()
        * 100
    )

    analysis = analysis.sort_values(
        "revenue",
        ascending=False
    )

    return analysis


def main():

    print("\n" + "=" * 60)
    print("MODIFIER ANALYSIS")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    analysis = create_modifier_analysis(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    analysis.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nPOS transactions: {len(df)}")
    print(f"Modifiers analyzed: {len(analysis)}")

    print("\nModifier summary:")
    print(
        analysis.to_string(index=False)
    )

    print("\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()