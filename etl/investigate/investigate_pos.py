import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from etl.extract import load_raw_data


def main():
    pos_data, _ = load_raw_data()

    df = pos_data.copy()

    # Calculate the simple expected total
    df["calculated_total"] = (
        df["quantity"] * df["unit_price"]
        - df["discount"].fillna(0)
        + df["tax"].fillna(0)
    )

    df["total_difference"] = df["total_amount"] - df["calculated_total"]

    # Only rows where total_amount exists
    valid = df[df["total_amount"].notna()].copy()

    # Identify matching vs mismatching transactions
    valid["matches_formula"] = valid["total_difference"].abs() <= 0.01

    print("\n" + "=" * 60)
    print("TOTAL AMOUNT INVESTIGATION")
    print("=" * 60)

    print("\n--- Overall ---")

    print(f"Transactions with total: {len(valid)}")
    print(f"Matching formula: {valid['matches_formula'].sum()}")
    print(f"Not matching formula: {(~valid['matches_formula']).sum()}")

    # Modifier comparison
    print("\n--- Modifier Analysis ---")

    modifier_analysis = (
        valid
        .groupby(valid["modifier"].fillna("No Modifier"))
        .agg(
            transactions=("order_id", "count"),
            mismatches=("matches_formula", lambda x: (~x).sum()),
            avg_difference=("total_difference", "mean"),
        )
        .sort_values("mismatches", ascending=False)
    )

    print(modifier_analysis.to_string())

    # Show biggest mismatches
    print("\n--- Largest Total Differences ---")

    columns = [
        "order_id",
        "menu_item",
        "modifier",
        "quantity",
        "unit_price",
        "discount",
        "tax",
        "total_amount",
        "calculated_total",
        "total_difference",
    ]

    largest = (
        valid
        .assign(abs_difference=valid["total_difference"].abs())
        .sort_values("abs_difference", ascending=False)
        .head(20)
    )

    print(largest[columns].to_string(index=False))


if __name__ == "__main__":
    main()