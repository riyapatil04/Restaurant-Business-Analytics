import sys
from pathlib import Path

import pandas as pd


# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from etl.extract import load_raw_data


def validate_pos(pos_df, menu_df):
    """Validate POS dataset and return a report dict."""
    report = {}

    # Rule 1: order_id uniqueness
    report["order_id_count"] = len(pos_df)
    report["order_id_unique_count"] = pos_df["order_id"].nunique()

    # Rule 2: quantity > 0
    report["quantity_leq_0"] = int((pos_df["quantity"] <= 0).sum())

    # Rule 3: unit_price > 0
    report["negative_unit_price"] = int((pos_df["unit_price"] < 0).sum())

    # Rule 4: discount >= 0 (allow missing, just flag negatives)
    report["negative_discount"] = int((pos_df["discount"] < 0).sum())
    report["missing_discount"] = int(pos_df["discount"].isna().sum())

    # Rule 5: tax >= 0
    report["negative_tax"] = int((pos_df["tax"] < 0).sum())
    report["missing_tax"] = int(pos_df["tax"].isna().sum())

    # Rule 6: total_amount >= 0
    report["negative_total_amount"] = int((pos_df["total_amount"] < 0).sum())
    report["missing_total_amount"] = int(pos_df["total_amount"].isna().sum())

    # Rule 7: service_mode
    valid_service_modes = {"Dine-In", "Drive-Thru", "Takeout", "Delivery"}
    report["missing_service_mode"] = int(pos_df["service_mode"].isna().sum())
    invalid_service = pos_df["service_mode"].dropna()
    invalid_service = invalid_service[~invalid_service.isin(valid_service_modes)]
    report["invalid_service_mode_count"] = int(invalid_service.shape[0])
    if invalid_service.shape[0] > 0:
        report["invalid_service_mode_values"] = list(invalid_service.unique())

    # Rule 8: payment_type
    valid_payment_types = {"Card", "Cash", "MobilePay", "GiftCard"}
    report["missing_payment_type"] = int(pos_df["payment_type"].isna().sum())
    invalid_payment = pos_df["payment_type"].dropna()
    invalid_payment = invalid_payment[~invalid_payment.isin(valid_payment_types)]
    report["invalid_payment_type_count"] = int(invalid_payment.shape[0])
    if invalid_payment.shape[0] > 0:
        report["invalid_payment_type_values"] = list(invalid_payment.unique())

    # Rule 9: menu items exist in menu COGS
    pos_items = set(pos_df["menu_item"].dropna().unique())
    menu_items = set(menu_df["menu_item"].dropna().unique())
    missing_in_menu = pos_items - menu_items
    report["pos_menu_items_count"] = len(pos_items)
    report["menu_cogs_items_count"] = len(menu_items)
    report["pos_items_not_in_menu_cogs"] = list(missing_in_menu) if missing_in_menu else []

    return report


def validate_menu(menu_df):
    """Validate menu COGS dataset and return a report dict."""
    report = {}

    # Rule 10: menu_item uniqueness
    report["menu_item_count"] = len(menu_df)
    report["menu_item_unique_count"] = menu_df["menu_item"].nunique()

    # Rule 11: selling_price > 0
    report["negative_selling_price"] = int((menu_df["selling_price"] < 0).sum())

    # Rule 12: costs >= 0
    report["negative_ingredient_cost"] = int((menu_df["ingredient_cost"] < 0).sum())
    report["negative_packaging_cost"] = int((menu_df["packaging_cost"] < 0).sum())
    report["negative_labor_cost"] = int((menu_df["labor_cost"] < 0).sum())
    report["negative_total_cogs"] = int((menu_df["total_cogs"] < 0).sum())

    # Rule 12a: check total_cogs ≈ ingredient + packaging + labor
    computed_cogs = (
        menu_df["ingredient_cost"]
        + menu_df["packaging_cost"]
        + menu_df["labor_cost"]
    )
    diff = (computed_cogs - menu_df["total_cogs"]).abs()
    report["total_cogs_mismatch_count"] = int((diff > 1e-6).sum())
    if report["total_cogs_mismatch_count"] > 0:
        report["total_cogs_mismatch_rows"] = menu_df.loc[diff > 1e-6, "menu_item"].tolist()

        # Rule 12b: food_cost_pct consistency (based on total_cogs, not ingredient_cost)
    computed_food_pct = (menu_df["total_cogs"] / menu_df["selling_price"]) * 100
    pct_diff = (computed_food_pct - menu_df["food_cost_pct"]).abs()
    report["food_cost_pct_mismatch_count"] = int((pct_diff > 1.0).sum())  # allow 1% tolerance
    if report["food_cost_pct_mismatch_count"] > 0:
        report["food_cost_pct_mismatch_rows"] = menu_df.loc[pct_diff > 1.0, "menu_item"].tolist()

    return report


def print_validation_report(pos_report, menu_report):
    print("\n" + "=" * 60)
    print("POS VALIDATION REPORT")
    print("=" * 60)

    print("\nOrder ID:")
    print(f"  Total rows: {pos_report['order_id_count']}")
    print(f"  Unique order_id: {pos_report['order_id_unique_count']}")

    print("\nQuantity:")
    print(f"  quantity <= 0: {pos_report['quantity_leq_0']}")

    print("\nPrices & amounts:")
    print(f"  negative_unit_price: {pos_report['negative_unit_price']}")
    print(f"  negative_discount: {pos_report['negative_discount']}")
    print(f"  missing_discount: {pos_report['missing_discount']}")
    print(f"  negative_tax: {pos_report['negative_tax']}")
    print(f"  missing_tax: {pos_report['missing_tax']}")
    print(f"  negative_total_amount: {pos_report['negative_total_amount']}")
    print(f"  missing_total_amount: {pos_report['missing_total_amount']}")

    print("\nService mode:")
    print(f"  missing_service_mode: {pos_report['missing_service_mode']}")
    print(f"  invalid_service_mode_count: {pos_report['invalid_service_mode_count']}")
    if pos_report.get("invalid_service_mode_values"):
        print(f"  invalid_service_mode_values: {pos_report['invalid_service_mode_values']}")

    print("\nPayment type:")
    print(f"  missing_payment_type: {pos_report['missing_payment_type']}")
    print(f"  invalid_payment_type_count: {pos_report['invalid_payment_type_count']}")
    if pos_report.get("invalid_payment_type_values"):
        print(f"  invalid_payment_type_values: {pos_report['invalid_payment_type_values']}")

    print("\nMenu items:")
    print(f"  POS menu items: {pos_report['pos_menu_items_count']}")
    print(f"  Menu COGS items: {pos_report['menu_cogs_items_count']}")
    if pos_report.get("pos_items_not_in_menu_cogs"):
        print(f"  POS items not in menu_cogs: {pos_report['pos_items_not_in_menu_cogs']}")
    else:
        print("  All POS menu items exist in menu_cogs.")

    print("\n" + "=" * 60)
    print("MENU COGS VALIDATION REPORT")
    print("=" * 60)

    print("\nMenu items:")
    print(f"  Total rows: {menu_report['menu_item_count']}")
    print(f"  Unique menu_item: {menu_report['menu_item_unique_count']}")

    print("\nPrices & costs:")
    print(f"  negative_selling_price: {menu_report['negative_selling_price']}")
    print(f"  negative_ingredient_cost: {menu_report['negative_ingredient_cost']}")
    print(f"  negative_packaging_cost: {menu_report['negative_packaging_cost']}")
    print(f"  negative_labor_cost: {menu_report['negative_labor_cost']}")
    print(f"  negative_total_cogs: {menu_report['negative_total_cogs']}")

    print("\nCOGS consistency:")
    print(f"  total_cogs mismatch count: {menu_report['total_cogs_mismatch_count']}")
    if menu_report.get("total_cogs_mismatch_rows"):
        print(f"  mismatched items: {menu_report['total_cogs_mismatch_rows']}")

    print("\nFood cost % consistency:")
    print(f"  food_cost_pct mismatch count: {menu_report['food_cost_pct_mismatch_count']}")
    if menu_report.get("food_cost_pct_mismatch_rows"):
        print(f"  mismatched items: {menu_report['food_cost_pct_mismatch_rows']}")


def main():
    pos_df, menu_df = load_raw_data()

    pos_report = validate_pos(pos_df, menu_df)
    menu_report = validate_menu(menu_df)

    print_validation_report(pos_report, menu_report)


if __name__ == "__main__":
    main()