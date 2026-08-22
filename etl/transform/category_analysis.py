import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))


MENU_ANALYSIS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "analytics"
    / "menu_analysis.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "analytics"
)

OUTPUT_FILE = OUTPUT_DIR / "category_analysis.csv"


def create_category_analysis(df):
    """Create category-level sales and profitability analysis."""

    category_analysis = (
        df.groupby("category")
        .agg(
            items=("menu_item", "nunique"),
            orders=("orders", "sum"),
            quantity_sold=("quantity_sold", "sum"),
            revenue=("revenue", "sum"),
            total_cost=("total_cost", "sum"),
            ingredient_cost=("ingredient_cost", "sum")
        )
        .reset_index()
    )

    category_analysis["gross_profit"] = (
        category_analysis["revenue"]
        - category_analysis["total_cost"]
    )

    category_analysis["profit_margin_pct"] = (
        category_analysis["gross_profit"]
        / category_analysis["revenue"]
        * 100
    )

    category_analysis["food_cost_pct"] = (
        category_analysis["ingredient_cost"]
        / category_analysis["revenue"]
        * 100
    )

    category_analysis["avg_revenue_per_order"] = (
        category_analysis["revenue"]
        / category_analysis["orders"]
    )

    category_analysis = category_analysis.sort_values(
        "gross_profit",
        ascending=False
    )

    return category_analysis


def main():

    print("\n" + "=" * 60)
    print("CATEGORY SALES & PROFIT ANALYSIS")
    print("=" * 60)

    df = pd.read_csv(MENU_ANALYSIS_FILE)

    category_analysis = create_category_analysis(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    category_analysis.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nMenu items: {df['menu_item'].nunique()}")
    print(f"Categories analyzed: {len(category_analysis)}")

    print("\nCategory summary:")

    print(
        category_analysis[
            [
                "category",
                "items",
                "orders",
                "quantity_sold",
                "revenue",
                "total_cost",
                "gross_profit",
                "profit_margin_pct",
                "food_cost_pct"
            ]
        ]
        .to_string(index=False)
    )

    print("\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()