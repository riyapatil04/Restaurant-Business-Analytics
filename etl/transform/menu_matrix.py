import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))


INPUT_FILE = (
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

OUTPUT_FILE = OUTPUT_DIR / "menu_matrix.csv"


def create_menu_matrix(df):
    """Classify menu items by sales volume and profitability."""

    sales_median = df["quantity_sold"].median()
    profit_median = df["profit_margin_pct"].median()

    df["sales_level"] = df["quantity_sold"].apply(
        lambda x: "High" if x >= sales_median else "Low"
    )

    df["profitability_level"] = df["profit_margin_pct"].apply(
        lambda x: "High" if x >= profit_median else "Low"
    )

    def classify(row):
        if (
            row["sales_level"] == "High"
            and row["profitability_level"] == "High"
        ):
            return "Star"

        elif (
            row["sales_level"] == "High"
            and row["profitability_level"] == "Low"
        ):
            return "Problem Child"

        elif (
            row["sales_level"] == "Low"
            and row["profitability_level"] == "High"
        ):
            return "Hidden Gem"

        else:
            return "Dog"

    df["menu_classification"] = df.apply(
        classify,
        axis=1
    )

    return df


def main():

    print("\n" + "=" * 60)
    print("MENU PERFORMANCE MATRIX")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    menu_matrix = create_menu_matrix(df)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    menu_matrix.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"\nSales median: "
        f"{df['quantity_sold'].median():.2f}"
    )

    print(
        f"Profit margin median: "
        f"{df['profit_margin_pct'].median():.2f}%"
    )

    print("\nClassification counts:")

    print(
        menu_matrix["menu_classification"]
        .value_counts()
        .to_string()
    )

    print("\nMenu matrix:")

    print(
        menu_matrix[
            [
                "menu_item",
                "category",
                "quantity_sold",
                "revenue",
                "gross_profit",
                "profit_margin_pct",
                "sales_level",
                "profitability_level",
                "menu_classification"
            ]
        ]
        .sort_values(
            "quantity_sold",
            ascending=False
        )
        .to_string(index=False)
    )

    print("\nSaved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()