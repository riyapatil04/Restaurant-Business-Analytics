from pathlib import Path
import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

POS_FILE = PROJECT_ROOT / "data" / "processed" / "qsr_pos_enriched.csv"
COGS_FILE = PROJECT_ROOT / "data" / "processed" / "menu_cogs_cleaned.csv"

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "analytics"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "profitability_summary.csv"
CATEGORY_OUTPUT_FILE = OUTPUT_DIR / "profitability_by_category.csv"


# ============================================================
# LOAD DATA
# ============================================================

pos = pd.read_csv(POS_FILE)
cogs = pd.read_csv(COGS_FILE)


# ============================================================
# PREPARE DATA
# ============================================================

# Treat missing discounts as zero
pos["discount"] = pos["discount"].fillna(0)

# Calculate revenue using total_amount where available.
# If total_amount is missing, calculate from quantity, price,
# discount and tax.
pos["calculated_subtotal"] = (
    pos["quantity"] * pos["unit_price"]
) - pos["discount"]

pos["calculated_revenue"] = (
    pos["calculated_subtotal"] + pos["tax"].fillna(0)
)

pos["revenue"] = pos["total_amount"].fillna(
    pos["calculated_revenue"]
)

# Ensure numeric columns are numeric
pos["quantity"] = pd.to_numeric(pos["quantity"], errors="coerce").fillna(0)
pos["discount"] = pd.to_numeric(pos["discount"], errors="coerce").fillna(0)
pos["revenue"] = pd.to_numeric(pos["revenue"], errors="coerce").fillna(0)

cogs["total_cogs"] = pd.to_numeric(
    cogs["total_cogs"], errors="coerce"
).fillna(0)


# ============================================================
# MERGE POS WITH COGS
# ============================================================

df = pos.merge(
    cogs[
        [
            "menu_item",
            "category",
            "ingredient_cost",
            "packaging_cost",
            "labor_cost",
            "total_cogs",
            "food_cost_pct",
        ]
    ],
    on="menu_item",
    how="left"
)


# ============================================================
# TRANSACTION-LEVEL PROFITABILITY
# ============================================================

df["total_cost"] = df["quantity"] * df["total_cogs"]

df["gross_profit"] = df["revenue"] - df["total_cost"]

total_revenue = df["revenue"].sum()
total_cost = df["total_cost"].sum()
gross_profit = df["gross_profit"].sum()

gross_margin = (
    gross_profit / total_revenue * 100
    if total_revenue != 0
    else 0
)

total_orders = df["order_id"].nunique()
total_units = df["quantity"].sum()

avg_order_value = (
    total_revenue / total_orders
    if total_orders != 0
    else 0
)


# ============================================================
# OVERALL PROFITABILITY SUMMARY
# ============================================================

summary = pd.DataFrame(
    [
        {
            "metric": "Total Revenue",
            "value": total_revenue,
        },
        {
            "metric": "Total COGS",
            "value": total_cost,
        },
        {
            "metric": "Gross Profit",
            "value": gross_profit,
        },
        {
            "metric": "Gross Margin %",
            "value": gross_margin,
        },
        {
            "metric": "Total Orders",
            "value": total_orders,
        },
        {
            "metric": "Total Units Sold",
            "value": total_units,
        },
        {
            "metric": "Average Order Value",
            "value": avg_order_value,
        },
    ]
)

summary.to_csv(OUTPUT_FILE, index=False)


# ============================================================
# CATEGORY PROFITABILITY
# ============================================================

category = (
    df.groupby("category")
    .agg(
        orders=("order_id", "nunique"),
        quantity_sold=("quantity", "sum"),
        revenue=("revenue", "sum"),
        total_cogs=("total_cost", "sum"),
    )
    .reset_index()
)

category["gross_profit"] = (
    category["revenue"] - category["total_cogs"]
)

category["profit_margin_pct"] = (
    category["gross_profit"]
    / category["revenue"]
    * 100
)

category["revenue_share_pct"] = (
    category["revenue"]
    / category["revenue"].sum()
    * 100
)

category = category.sort_values(
    "gross_profit",
    ascending=False
)

category.to_csv(
    CATEGORY_OUTPUT_FILE,
    index=False
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("=" * 60)
print("PROFITABILITY SUMMARY")
print("=" * 60)

print(f"\nTotal Revenue:     ${total_revenue:,.2f}")
print(f"Total COGS:        ${total_cost:,.2f}")
print(f"Gross Profit:      ${gross_profit:,.2f}")
print(f"Gross Margin:      {gross_margin:.2f}%")
print(f"Total Orders:      {total_orders:,}")
print(f"Total Units Sold:  {total_units:,.0f}")
print(f"Average Order:     ${avg_order_value:.2f}")

print("\n--- CATEGORY PROFITABILITY ---")

print(
    category[
        [
            "category",
            "revenue",
            "total_cogs",
            "gross_profit",
            "profit_margin_pct",
            "revenue_share_pct",
        ]
    ].to_string(index=False)
)

print("\nSaved files:")
print(OUTPUT_FILE)
print(CATEGORY_OUTPUT_FILE)