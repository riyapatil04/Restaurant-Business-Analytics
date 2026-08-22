import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))


POS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "qsr_pos_enriched.csv"
)

COGS_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "menu_cogs_cleaned.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "analytics"
)

OUTPUT_FILE = OUTPUT_DIR / "menu_analysis.csv"


def create_menu_analysis(pos_df, cogs_df):
    """Combine POS sales with menu cost information."""

    # Aggregate POS transactions by menu item
    menu_sales = (
        pos_df.groupby("menu_item")
        .agg(
            orders=("order_id", "count"),
            quantity_sold=("quantity", "sum"),
            revenue=("total_amount", "sum"),
            discount=("discount", "sum")
        )
        .reset_index()
    )

    # Join sales data with menu COGS data
    menu_analysis = menu_sales.merge(
        cogs_df[
            [
                "menu_item",
                "category",
                "selling_price",
                "ingredient_cost",
                "packaging_cost",
                "labor_cost",
                "total_cogs",
                "food_cost_pct",
                "supplier"
            ]
        ],
        on="menu_item",
        how="left"
    )

    # Estimate total COGS based on quantity sold
    menu_analysis["total_cost"] = (
        menu_analysis["quantity_sold"]
        * menu_analysis["total_cogs"]
    )

    # Calculate gross profit
    menu_analysis["gross_profit"] = (
        menu_analysis["revenue"]
        - menu_analysis["total_cost"]
    )

    # Calculate profit margin
    menu_analysis["profit_margin_pct"] = (
        menu_analysis["gross_profit"]
        / menu_analysis["revenue"]
        * 100
    )

    # Average revenue per order
    menu_analysis["avg_revenue_per_order"] = (
        menu_analysis["revenue"]
        / menu_analysis["orders"]
    )

    # Sort by revenue
    menu_analysis = menu_analysis.sort_values(
        "revenue",
        ascending=False
    )

    return menu_analysis


def main():

    print("\n" + "=" * 60)
    print("MENU SALES & PROFIT ANALYSIS")
    print("=" * 60)

    # Load datasets
    pos_df = pd.read_csv(POS_FILE)
    cogs_df = pd.read_csv(COGS_FILE)

    # Create analysis
    menu_analysis = create_menu_analysis(
        pos_df,
        cogs_df
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save result
    menu_analysis.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nPOS transactions: {len(pos_df)}")
    print(f"Menu items analyzed: {len(menu_analysis)}")

    print("\nColumns:")
    print(list(menu_analysis.columns))

    print("\nTop menu items by revenue:")
    print(
        menu_analysis[
            [
                "menu_item",
                "category",
                "quantity_sold",
                "revenue",
                "total_cost",
                "gross_profit",
                "profit_margin_pct"
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    print("\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()