from pathlib import Path
import pandas as pd


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

COGS_FILE = PROJECT_ROOT / "data" / "processed" / "menu_cogs_cleaned.csv"
MENU_ANALYSIS_FILE = (
    PROJECT_ROOT / "data" / "processed" / "analytics" / "menu_analysis.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "analytics"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "menu_cost_analysis.csv"


# ============================================================
# LOAD DATA
# ============================================================

cogs = pd.read_csv(COGS_FILE)
menu = pd.read_csv(MENU_ANALYSIS_FILE)


# ============================================================
# PREPARE COGS DATA
# ============================================================

numeric_columns = [
    "selling_price",
    "ingredient_cost",
    "packaging_cost",
    "labor_cost",
    "total_cogs",
    "food_cost_pct",
]

for column in numeric_columns:
    cogs[column] = pd.to_numeric(
        cogs[column],
        errors="coerce"
    ).fillna(0)


# ============================================================
# MERGE WITH SALES PERFORMANCE
# ============================================================

df = cogs.merge(
    menu[
        [
            "menu_item",
            "orders",
            "quantity_sold",
            "revenue",
            "gross_profit",
            "profit_margin_pct",
        ]
    ],
    on="menu_item",
    how="left"
)

df["orders"] = df["orders"].fillna(0)
df["quantity_sold"] = df["quantity_sold"].fillna(0)
df["revenue"] = df["revenue"].fillna(0)
df["gross_profit"] = df["gross_profit"].fillna(0)
df["profit_margin_pct"] = df["profit_margin_pct"].fillna(0)


# ============================================================
# COST STRUCTURE
# ============================================================

df["ingredient_cost_pct"] = (
    df["ingredient_cost"]
    / df["selling_price"]
    * 100
)

df["packaging_cost_pct"] = (
    df["packaging_cost"]
    / df["selling_price"]
    * 100
)

df["labor_cost_pct"] = (
    df["labor_cost"]
    / df["selling_price"]
    * 100
)

df["total_cogs_pct"] = (
    df["total_cogs"]
    / df["selling_price"]
    * 100
)


# ============================================================
# COST RANKINGS
# ============================================================

food_cost_median = df["food_cost_pct"].median()
cogs_median = df["total_cogs"].median()

df["food_cost_level"] = df["food_cost_pct"].apply(
    lambda x: "High" if x > food_cost_median else "Low"
)

df["cogs_level"] = df["total_cogs"].apply(
    lambda x: "High" if x > cogs_median else "Low"
)


# ============================================================
# COST EFFICIENCY
# ============================================================

df["profit_per_unit"] = (
    df["selling_price"] - df["total_cogs"]
)

df["cost_to_price_ratio"] = (
    df["total_cogs"]
    / df["selling_price"]
)


# ============================================================
# IDENTIFY HIGH-COST ITEMS
# ============================================================

food_cost_threshold = df["food_cost_pct"].quantile(0.75)

df["high_food_cost_flag"] = (
    df["food_cost_pct"] >= food_cost_threshold
)


# ============================================================
# FINAL COLUMNS
# ============================================================

output_columns = [
    "menu_item",
    "category",
    "selling_price",
    "ingredient_cost",
    "packaging_cost",
    "labor_cost",
    "total_cogs",
    "food_cost_pct",
    "ingredient_cost_pct",
    "packaging_cost_pct",
    "labor_cost_pct",
    "total_cogs_pct",
    "profit_per_unit",
    "cost_to_price_ratio",
    "orders",
    "quantity_sold",
    "revenue",
    "gross_profit",
    "profit_margin_pct",
    "food_cost_level",
    "cogs_level",
    "high_food_cost_flag",
]

df = df[output_columns].sort_values(
    "food_cost_pct",
    ascending=False
)


# ============================================================
# SAVE
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# DISPLAY
# ============================================================

print("=" * 60)
print("MENU COST ANALYSIS")
print("=" * 60)

print(f"\nMenu items analyzed: {len(df)}")
print(f"Median food cost %: {food_cost_median:.2f}%")
print(f"Median total COGS: ${cogs_median:.2f}")

print("\n--- HIGHEST FOOD-COST ITEMS ---")

print(
    df[
        [
            "menu_item",
            "category",
            "selling_price",
            "total_cogs",
            "food_cost_pct",
            "profit_margin_pct",
        ]
    ]
    .head(10)
    .to_string(index=False)
)

print("\n--- COST STRUCTURE ---")

print(
    df[
        [
            "menu_item",
            "ingredient_cost_pct",
            "packaging_cost_pct",
            "labor_cost_pct",
            "total_cogs_pct",
        ]
    ]
    .head(10)
    .to_string(index=False)
)

print("\n--- HIGH FOOD-COST ITEMS ---")

high_cost = df[df["high_food_cost_flag"]]

print(
    high_cost[
        [
            "menu_item",
            "food_cost_pct",
            "total_cogs",
            "profit_margin_pct",
        ]
    ].to_string(index=False)
)

print("\nSaved to:")
print(OUTPUT_FILE)