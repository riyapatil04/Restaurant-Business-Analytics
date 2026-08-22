import pandas as pd
from pathlib import Path


# ============================================================
# SALES TREND ANALYSIS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

INPUT_FILE = BASE_DIR / "data" / "processed" / "analytics" / "sales_monthly.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed" / "analytics" / "sales"
OUTPUT_FILE = OUTPUT_DIR / "sales_trend_analysis.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

df["date"] = pd.to_datetime(
    df["year"].astype(str) + "-" +
    df["month"].astype(str) + "-01"
)

df = df.sort_values("date").reset_index(drop=True)


# ------------------------------------------------------------
# MONTHLY TREND METRICS
# ------------------------------------------------------------

df["revenue_growth_pct"] = (
    df["revenue"].pct_change() * 100
)

df["orders_growth_pct"] = (
    df["orders"].pct_change() * 100
)

df["aov_growth_pct"] = (
    df["avg_order_value"].pct_change() * 100
)

df["rolling_3m_revenue"] = (
    df["revenue"].rolling(3, min_periods=1).mean()
)

df["rolling_3m_orders"] = (
    df["orders"].rolling(3, min_periods=1).mean()
)

df["rolling_3m_aov"] = (
    df["avg_order_value"].rolling(3, min_periods=1).mean()
)


# ------------------------------------------------------------
# TREND CLASSIFICATION
# ------------------------------------------------------------

def classify_trend(growth):
    if pd.isna(growth):
        return "Baseline"
    elif growth > 5:
        return "Strong Growth"
    elif growth > 0:
        return "Growth"
    elif growth < -5:
        return "Strong Decline"
    else:
        return "Decline"


df["revenue_trend"] = df["revenue_growth_pct"].apply(classify_trend)


# ------------------------------------------------------------
# PERIOD LABEL
# ------------------------------------------------------------

df["period"] = (
    df["month_name"].astype(str)
    + " "
    + df["year"].astype(str)
)


# ------------------------------------------------------------
# SELECT OUTPUT COLUMNS
# ------------------------------------------------------------

result = df[
    [
        "year",
        "month",
        "month_name",
        "period",
        "orders",
        "units_sold",
        "revenue",
        "discount",
        "avg_order_value",
        "revenue_growth_pct",
        "orders_growth_pct",
        "aov_growth_pct",
        "rolling_3m_revenue",
        "rolling_3m_orders",
        "rolling_3m_aov",
        "revenue_trend",
    ]
].copy()


# ------------------------------------------------------------
# ROUND VALUES
# ------------------------------------------------------------

numeric_columns = [
    "revenue",
    "discount",
    "avg_order_value",
    "revenue_growth_pct",
    "orders_growth_pct",
    "aov_growth_pct",
    "rolling_3m_revenue",
    "rolling_3m_orders",
    "rolling_3m_aov",
]

result[numeric_columns] = result[numeric_columns].round(2)


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

result.to_csv(OUTPUT_FILE, index=False)


# ------------------------------------------------------------
# REPORT
# ------------------------------------------------------------

print("=" * 60)
print("SALES TREND ANALYSIS")
print("=" * 60)

print(f"\nMonths analyzed: {len(result)}")

print("\nMonthly trend:")
print(
    result[
        [
            "period",
            "orders",
            "revenue",
            "avg_order_value",
            "revenue_growth_pct",
            "rolling_3m_revenue",
            "revenue_trend",
        ]
    ].to_string(index=False)
)

valid_growth = result.dropna(subset=["revenue_growth_pct"])

if not valid_growth.empty:
    strongest_growth = valid_growth.loc[
        valid_growth["revenue_growth_pct"].idxmax()
    ]

    strongest_decline = valid_growth.loc[
        valid_growth["revenue_growth_pct"].idxmin()
    ]

    print("\n--- KEY TREND INSIGHTS ---")
    print(
        f"Strongest growth: "
        f"{strongest_growth['period']} "
        f"({strongest_growth['revenue_growth_pct']:.2f}%)"
    )

    print(
        f"Strongest decline: "
        f"{strongest_decline['period']} "
        f"({strongest_decline['revenue_growth_pct']:.2f}%)"
    )

if len(result) >= 2:
    first_revenue = result.iloc[0]["revenue"]
    last_revenue = result.iloc[-1]["revenue"]

    total_growth = (
        (last_revenue - first_revenue)
        / first_revenue
        * 100
    )

    print(
        f"Overall revenue change: {total_growth:.2f}%"
    )

print("\nSaved to:")
print(OUTPUT_FILE)