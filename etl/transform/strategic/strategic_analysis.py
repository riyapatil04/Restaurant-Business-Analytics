import pandas as pd
from pathlib import Path


# ============================================================
# STRATEGIC ANALYSIS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

DISCOUNT_FILE = (
    BASE_DIR / "data" / "processed" / "analytics" / "discount_analysis.csv"
)

MENU_FILE = (
    BASE_DIR / "data" / "processed" / "analytics" / "menu_matrix.csv"
)

OUTPUT_DIR = BASE_DIR / "data" / "processed" / "analytics" / "strategic"
OUTPUT_FILE = OUTPUT_DIR / "strategic_analysis.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

discount = pd.read_csv(DISCOUNT_FILE)
menu = pd.read_csv(MENU_FILE)


# ------------------------------------------------------------
# DISCOUNT ANALYSIS
# ------------------------------------------------------------

discounted = discount[
    discount["discount_status"] == "Discounted"
].iloc[0]

normal = discount[
    discount["discount_status"] == "No Discount"
].iloc[0]

discount_aov = discounted["avg_order_value"]
normal_aov = normal["avg_order_value"]

aov_difference_pct = (
    (discount_aov - normal_aov)
    / normal_aov
    * 100
)

discounted_revenue_share = discounted["revenue_share_pct"]
discounted_order_share = discounted["discounted_order_share_pct"]

discount_rate = (
    discounted["total_discount"]
    / (discounted["revenue"] + discounted["total_discount"])
    * 100
)


# ------------------------------------------------------------
# MENU STRATEGIC FLAGS
# ------------------------------------------------------------

def strategic_action(row):

    classification = row["menu_classification"]

    if classification == "Star":
        return "Promote / Protect"

    if classification == "Problem Child":
        return "Improve Margin"

    if classification == "Hidden Gem":
        return "Increase Visibility"

    if classification == "Dog":
        return "Review / Consider Removal"

    return "Monitor"


menu["strategic_action"] = menu.apply(
    strategic_action,
    axis=1
)


# ------------------------------------------------------------
# PRIORITY SCORE
# ------------------------------------------------------------

menu["priority_score"] = 0

menu.loc[
    menu["menu_classification"] == "Problem Child",
    "priority_score"
] = 3

menu.loc[
    menu["menu_classification"] == "Dog",
    "priority_score"
] = 2

menu.loc[
    menu["menu_classification"] == "Hidden Gem",
    "priority_score"
] = 2

menu.loc[
    menu["menu_classification"] == "Star",
    "priority_score"
] = 1


# ------------------------------------------------------------
# CREATE STRATEGIC MENU DATASET
# ------------------------------------------------------------

menu_output = menu[
    [
        "menu_item",
        "category",
        "quantity_sold",
        "revenue",
        "gross_profit",
        "profit_margin_pct",
        "sales_level",
        "profitability_level",
        "menu_classification",
        "strategic_action",
        "priority_score",
    ]
].copy()


menu_output = menu_output.sort_values(
    ["priority_score", "revenue"],
    ascending=[False, False]
)


# ------------------------------------------------------------
# SAVE MENU STRATEGY
# ------------------------------------------------------------

MENU_OUTPUT_FILE = (
    OUTPUT_DIR / "strategic_menu_analysis.csv"
)

menu_output.to_csv(
    MENU_OUTPUT_FILE,
    index=False
)


# ------------------------------------------------------------
# CREATE STRATEGIC SUMMARY
# ------------------------------------------------------------

summary = pd.DataFrame(
    [
        {
            "metric": "Discounted Orders",
            "value": discounted["orders"],
        },
        {
            "metric": "Discounted Order Share %",
            "value": discounted_order_share,
        },
        {
            "metric": "Discounted Revenue",
            "value": discounted["revenue"],
        },
        {
            "metric": "Discounted Revenue Share %",
            "value": discounted_revenue_share,
        },
        {
            "metric": "Total Discount Given",
            "value": discounted["total_discount"],
        },
        {
            "metric": "Discount Rate %",
            "value": discount_rate,
        },
        {
            "metric": "Discounted AOV",
            "value": discount_aov,
        },
        {
            "metric": "Normal AOV",
            "value": normal_aov,
        },
        {
            "metric": "AOV Difference %",
            "value": aov_difference_pct,
        },
        {
            "metric": "Star Items",
            "value": (menu["menu_classification"] == "Star").sum(),
        },
        {
            "metric": "Problem Child Items",
            "value": (
                menu["menu_classification"]
                == "Problem Child"
            ).sum(),
        },
        {
            "metric": "Hidden Gem Items",
            "value": (
                menu["menu_classification"]
                == "Hidden Gem"
            ).sum(),
        },
        {
            "metric": "Dog Items",
            "value": (menu["menu_classification"] == "Dog").sum(),
        },
    ]
)

summary["value"] = summary["value"].round(2)


# ------------------------------------------------------------
# SAVE SUMMARY
# ------------------------------------------------------------

summary.to_csv(
    OUTPUT_FILE,
    index=False
)


# ------------------------------------------------------------
# REPORT
# ------------------------------------------------------------

print("=" * 60)
print("STRATEGIC ANALYSIS")
print("=" * 60)

print("\n--- DISCOUNT STRATEGY ---")
print(f"Discounted orders: {discounted['orders']}")
print(f"Discounted order share: {discounted_order_share:.2f}%")
print(f"Discounted revenue: ${discounted['revenue']:.2f}")
print(f"Discounted revenue share: {discounted_revenue_share:.2f}%")
print(f"Total discount given: ${discounted['total_discount']:.2f}")
print(f"Discount rate: {discount_rate:.2f}%")
print(f"Discounted AOV: ${discount_aov:.2f}")
print(f"Normal AOV: ${normal_aov:.2f}")
print(f"AOV difference: {aov_difference_pct:.2f}%")

print("\n--- MENU STRATEGY ---")

print(
    "\nStars:",
    (menu["menu_classification"] == "Star").sum()
)

print(
    "Problem Children:",
    (menu["menu_classification"] == "Problem Child").sum()
)

print(
    "Hidden Gems:",
    (menu["menu_classification"] == "Hidden Gem").sum()
)

print(
    "Dogs:",
    (menu["menu_classification"] == "Dog").sum()
)

print("\n--- TOP PRIORITY ITEMS ---")

print(
    menu_output[
        [
            "menu_item",
            "menu_classification",
            "strategic_action",
            "revenue",
            "profit_margin_pct",
        ]
    ]
    .head(10)
    .to_string(index=False)
)

print("\nSaved files:")
print(OUTPUT_FILE)
print(MENU_OUTPUT_FILE)