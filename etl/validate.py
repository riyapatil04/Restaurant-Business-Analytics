from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw")


def read_dataset(filename):
    file_path = RAW_DIR / filename

    if filename.lower().endswith(".csv"):
        return pd.read_csv(file_path)
    else:
        raise ValueError(f"Unsupported file type: {filename}")


def validate_pos(df):
    issues = {}

    issues["negative_quantity"] = int((df["quantity"] < 0).sum()) if "quantity" in df.columns else None
    issues["zero_quantity"] = int((df["quantity"] == 0).sum()) if "quantity" in df.columns else None
    issues["negative_unit_price"] = int((df["unit_price"] < 0).sum()) if "unit_price" in df.columns else None
    issues["negative_discount"] = int((df["discount"] < 0).sum()) if "discount" in df.columns else None
    issues["negative_tax"] = int((df["tax"] < 0).sum()) if "tax" in df.columns else None
    issues["negative_total_amount"] = int((df["total_amount"] < 0).sum()) if "total_amount" in df.columns else None

    return issues


def validate_menu_cogs(df):
    issues = {}

    issues["negative_selling_price"] = int((df["selling_price"] < 0).sum()) if "selling_price" in df.columns else None
    issues["negative_ingredient_cost"] = int((df["ingredient_cost"] < 0).sum()) if "ingredient_cost" in df.columns else None
    issues["negative_packaging_cost"] = int((df["packaging_cost"] < 0).sum()) if "packaging_cost" in df.columns else None
    issues["negative_labor_cost"] = int((df["labor_cost"] < 0).sum()) if "labor_cost" in df.columns else None
    issues["negative_total_cogs"] = int((df["total_cogs"] < 0).sum()) if "total_cogs" in df.columns else None
    issues["food_cost_pct_out_of_range"] = int(
        ((df["food_cost_pct"] < 0) | (df["food_cost_pct"] > 100)).sum()
    ) if "food_cost_pct" in df.columns else None

    return issues


def main():
    pos = read_dataset("qsr_pos_logs.csv")
    menu = read_dataset("menu_cogs.csv")

    print("POS Validation:")
    print(validate_pos(pos))
    print("-" * 60)

    print("Menu COGS Validation:")
    print(validate_menu_cogs(menu))
    print("-" * 60)


if __name__ == "__main__":
    main()