import pandas as pd
from pathlib import Path


# ============================================================
# DASHBOARD MASTER DATASET
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

ANALYTICS_DIR = (
    BASE_DIR / "data" / "processed" / "analytics"
)

OUTPUT_DIR = ANALYTICS_DIR / "dashboard"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# FILE PATHS
# ------------------------------------------------------------

FILES = {
    "profitability": ANALYTICS_DIR / "profitability_summary.csv",
    "category": ANALYTICS_DIR / "profitability_by_category.csv",
    "monthly": ANALYTICS_DIR / "sales" / "sales_trend_analysis.csv",
    "menu": ANALYTICS_DIR / "menu_analysis.csv",
    "matrix": ANALYTICS_DIR / "menu_matrix.csv",
    "store": ANALYTICS_DIR / "store_analysis.csv",
    "service": ANALYTICS_DIR / "service_mode_analysis.csv",
    "daypart": ANALYTICS_DIR / "daypart_analysis.csv",
    "payment": ANALYTICS_DIR / "payment_analysis.csv",
    "discount": ANALYTICS_DIR / "discount_analysis.csv",
    "strategic_menu": (
        ANALYTICS_DIR
        / "strategic"
        / "strategic_menu_analysis.csv"
    ),
}


# ------------------------------------------------------------
# LOAD FILES
# ------------------------------------------------------------

data = {}

for name, path in FILES.items():

    if not path.exists():
        raise FileNotFoundError(
            f"Required file not found: {path}"
        )

    data[name] = pd.read_csv(path)


# ------------------------------------------------------------
# 1. KPI MASTER
# ------------------------------------------------------------

profitability = data["profitability"]

kpi = profitability.copy()

kpi["report_type"] = "Overall KPI"

kpi.to_csv(
    OUTPUT_DIR / "dashboard_kpis.csv",
    index=False
)


# ------------------------------------------------------------
# 2. MONTHLY TREND
# ------------------------------------------------------------

monthly = data["monthly"].copy()

monthly.to_csv(
    OUTPUT_DIR / "dashboard_monthly_trend.csv",
    index=False
)


# ------------------------------------------------------------
# 3. MENU PERFORMANCE
# ------------------------------------------------------------

menu = data["menu"].copy()

menu.to_csv(
    OUTPUT_DIR / "dashboard_menu_performance.csv",
    index=False
)


# ------------------------------------------------------------
# 4. MENU MATRIX
# ------------------------------------------------------------

matrix = data["matrix"].copy()

matrix.to_csv(
    OUTPUT_DIR / "dashboard_menu_matrix.csv",
    index=False
)


# ------------------------------------------------------------
# 5. CATEGORY PERFORMANCE
# ------------------------------------------------------------

category = data["category"].copy()

category.to_csv(
    OUTPUT_DIR / "dashboard_category_performance.csv",
    index=False
)


# ------------------------------------------------------------
# 6. STORE PERFORMANCE
# ------------------------------------------------------------

store = data["store"].copy()

store.to_csv(
    OUTPUT_DIR / "dashboard_store_performance.csv",
    index=False
)


# ------------------------------------------------------------
# 7. SERVICE MODE
# ------------------------------------------------------------

service = data["service"].copy()

service.to_csv(
    OUTPUT_DIR / "dashboard_service_mode.csv",
    index=False
)


# ------------------------------------------------------------
# 8. DAYPART
# ------------------------------------------------------------

daypart = data["daypart"].copy()

daypart.to_csv(
    OUTPUT_DIR / "dashboard_daypart.csv",
    index=False
)


# ------------------------------------------------------------
# 9. PAYMENT
# ------------------------------------------------------------

payment = data["payment"].copy()

payment.to_csv(
    OUTPUT_DIR / "dashboard_payment.csv",
    index=False
)


# ------------------------------------------------------------
# 10. DISCOUNT
# ------------------------------------------------------------

discount = data["discount"].copy()

discount.to_csv(
    OUTPUT_DIR / "dashboard_discount.csv",
    index=False
)


# ------------------------------------------------------------
# 11. STRATEGIC MENU
# ------------------------------------------------------------

strategic_menu = data["strategic_menu"].copy()

strategic_menu.to_csv(
    OUTPUT_DIR / "dashboard_strategic_menu.csv",
    index=False
)


# ------------------------------------------------------------
# 12. MASTER MENU DATASET
# ------------------------------------------------------------

master_menu = menu.merge(
    matrix[
        [
            "menu_item",
            "menu_classification",
            "sales_level",
            "profitability_level",
        ]
    ],
    on="menu_item",
    how="left"
)

master_menu = master_menu.merge(
    strategic_menu[
        [
            "menu_item",
            "strategic_action",
            "priority_score",
        ]
    ],
    on="menu_item",
    how="left"
)

master_menu.to_csv(
    OUTPUT_DIR / "dashboard_master_menu.csv",
    index=False
)


# ------------------------------------------------------------
# 13. MASTER DASHBOARD INDEX
# ------------------------------------------------------------

dashboard_index = pd.DataFrame(
    [
        {
            "dataset": "KPI Summary",
            "file": "dashboard_kpis.csv",
            "purpose": "Overall business KPIs",
        },
        {
            "dataset": "Monthly Trend",
            "file": "dashboard_monthly_trend.csv",
            "purpose": "Revenue and sales trends",
        },
        {
            "dataset": "Menu Performance",
            "file": "dashboard_menu_performance.csv",
            "purpose": "Menu sales and profitability",
        },
        {
            "dataset": "Menu Matrix",
            "file": "dashboard_menu_matrix.csv",
            "purpose": "Star / Problem Child / Hidden Gem / Dog",
        },
        {
            "dataset": "Master Menu",
            "file": "dashboard_master_menu.csv",
            "purpose": "Complete menu dashboard dataset",
        },
        {
            "dataset": "Category Performance",
            "file": "dashboard_category_performance.csv",
            "purpose": "Category revenue and profitability",
        },
        {
            "dataset": "Store Performance",
            "file": "dashboard_store_performance.csv",
            "purpose": "Store comparison",
        },
        {
            "dataset": "Service Mode",
            "file": "dashboard_service_mode.csv",
            "purpose": "Dine-in / Drive-thru / Takeout / Delivery",
        },
        {
            "dataset": "Daypart",
            "file": "dashboard_daypart.csv",
            "purpose": "Breakfast / Lunch / Dinner performance",
        },
        {
            "dataset": "Payment",
            "file": "dashboard_payment.csv",
            "purpose": "Payment method analysis",
        },
        {
            "dataset": "Discount",
            "file": "dashboard_discount.csv",
            "purpose": "Discount impact",
        },
        {
            "dataset": "Strategic Menu",
            "file": "dashboard_strategic_menu.csv",
            "purpose": "Strategic menu actions",
        },
    ]
)

dashboard_index.to_csv(
    OUTPUT_DIR / "dashboard_dataset_index.csv",
    index=False
)


# ------------------------------------------------------------
# REPORT
# ------------------------------------------------------------

print("=" * 60)
print("DASHBOARD MASTER DATASET")
print("=" * 60)

print("\nDashboard datasets created:")

for file in sorted(OUTPUT_DIR.glob("*.csv")):
    print(f"  - {file.name}")

print("\nTotal dashboard datasets:")
print(len(list(OUTPUT_DIR.glob("*.csv"))))

print("\nSaved to:")
print(OUTPUT_DIR)