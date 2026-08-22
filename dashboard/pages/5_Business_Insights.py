import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Business Insights", page_icon="💡", layout="wide")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ANALYTICS_PATH = PROJECT_ROOT / "data" / "processed" / "analytics"

@st.cache_data
def load_data():
    profitability = pd.read_csv(ANALYTICS_PATH / "profitability_summary.csv")
    category = pd.read_csv(ANALYTICS_PATH / "profitability_by_category.csv")
    monthly = pd.read_csv(ANALYTICS_PATH / "sales_monthly.csv")
    menu_matrix = pd.read_csv(ANALYTICS_PATH / "menu_matrix.csv")
    discount = pd.read_csv(ANALYTICS_PATH / "discount_analysis.csv")
    service = pd.read_csv(ANALYTICS_PATH / "service_mode_analysis.csv")
    daypart = pd.read_csv(ANALYTICS_PATH / "daypart_analysis.csv")
    store = pd.read_csv(ANALYTICS_PATH / "store_analysis.csv")
    return profitability, category, monthly, menu_matrix, discount, service, daypart, store

profitability, category, monthly, menu_matrix, discount, service, daypart, store = load_data()

st.title("💡 Business Insights")
st.caption("From descriptive analytics to actionable business decisions")
st.divider()

st.subheader("📋 Executive Summary")
kpi_dict = dict(zip(profitability["metric"], profitability["value"]))
total_revenue = kpi_dict.get("Total Revenue", 0)
gross_profit = kpi_dict.get("Gross Profit", 0)
gross_margin = kpi_dict.get("Gross Margin %", 0)
aov = kpi_dict.get("Average Order Value", 0)
best_category = category.loc[category["revenue"].idxmax()]
best_margin_category = category.loc[category["profit_margin_pct"].idxmax()]
best_daypart = daypart.loc[daypart["revenue"].idxmax()]
service_clean = service[service["service_mode"] != "Unknown"].copy()
best_service = service_clean.loc[service_clean["revenue"].idxmax()]
best_store = store.loc[store["revenue"].idxmax()]
st.markdown(f"""### Overall Business Health

The restaurant generated **** in revenue and **** in gross profit, producing a gross margin of **{gross_margin:.1f}%**.

The average order value is ****.

**{best_category["category"]}** is the largest revenue-generating category, while **{best_margin_category["category"]}** has the strongest category-level margin.

**{best_daypart["daypart"]}** is the strongest daypart and **{best_service["service_mode"]}** is the highest-revenue service mode.
""")

st.subheader("🏆 Business Strengths")
c1, c2, c3 = st.columns(3)
with c1:
    st.success(f"**Strong Overall Margin**\n\nGross margin:\n\n### {gross_margin:.1f}%\n\nThe restaurant retains a strong share of revenue after COGS.")
with c2:
    st.success(f"**Revenue Leader**\n\n{best_category['category']}\n\n### \n\nHighest revenue among categories.")
with c3:
    st.success(f"**Strongest Service Channel**\n\n{best_service['service_mode']}\n\n### \n\nHighest service-mode revenue.")

st.divider()
st.subheader("⚠️ Key Business Risks")
first_revenue = monthly.iloc[0]["revenue"]
last_revenue = monthly.iloc[-1]["revenue"]
overall_change = ((last_revenue / first_revenue) - 1) * 100
discounted = discount[discount["discount_status"] == "Discounted"].iloc[0]
normal = discount[discount["discount_status"] == "No Discount"].iloc[0]
discount_aov_change = ((discounted["avg_order_value"] / normal["avg_order_value"]) - 1) * 100
problem_children = menu_matrix[menu_matrix["menu_classification"] == "Problem Child"]
lowest_store = store.loc[store["revenue"].idxmin()]
risks = []
if overall_change < 0:
    risks.append(f"Revenue changed by **{overall_change:.1f}%** from the first to the latest observed month.")
if discount_aov_change < 0:
    risks.append(f"Discounted orders have a **{abs(discount_aov_change):.1f}% lower AOV** than non-discounted orders.")
if len(problem_children) > 0:
    risks.append(f"There are **{len(problem_children)} Problem Child menu items** that combine high sales with relatively weaker margins.")
risks.append(f"Store **{int(lowest_store['store_id'])}** has the lowest total revenue among the analyzed stores.")
for r in risks:
    st.warning(r)

st.divider()
st.subheader("🚀 Business Opportunities")
o1, o2 = st.columns(2)
with o1:
    st.markdown(f"""### 1. Increase Basket Size

Average order value is currently ****.

Most orders contain relatively few items, creating an opportunity to promote:

- Combos
- Sides
- Beverages
- Relevant modifiers

**Goal:** increase revenue per transaction without relying only on additional customer traffic.
""")
with o2:
    st.markdown(f"""### 2. Optimize High-Volume Items

**{len(problem_children)}** menu items are classified as Problem Children.

These products already generate demand but have weaker margins relative to the menu.

Possible actions:

- Review pricing
- Reduce ingredient costs
- Adjust portions
- Negotiate supplier costs
- Promote higher-margin add-ons
""")
o3, o4 = st.columns(2)
with o3:
    st.markdown(f"""### 3. Focus on Peak Periods

**{best_daypart['daypart']}** generates the most revenue:

****

Staffing, inventory and preparation should be optimized around these high-demand periods.
""")
with o4:
    st.markdown(f"""### 4. Evaluate Promotions

Discounted orders represent only a portion of total orders while having an AOV of ****.

Promotions should therefore be evaluated on **incremental profitability**, not simply the number of discounted orders.
""")

st.divider()
st.subheader("🎯 Highest-Priority Menu Items")
priority = problem_children.sort_values("revenue", ascending=False).head(10)
st.dataframe(priority[["menu_item","category","quantity_sold","revenue","gross_profit","profit_margin_pct"]], width="stretch", hide_index=True)
st.caption("These products have high sales volume but relatively weaker profitability and should be investigated first.")

st.divider()
st.subheader("🎯 Recommended Management Actions")
actions = [
    ("1", "Protect high-performing periods", f"Prioritize staffing and inventory during {best_daypart['daypart']}."),
    ("2", "Improve Problem Children", f"Review pricing and cost structure for {len(problem_children)} high-volume items."),
    ("3", "Increase basket size", "Use combos, sides, beverages and modifiers to increase AOV."),
    ("4", "Optimize promotions", "Measure discounts against incremental revenue and profit."),
    ("5", "Benchmark stores", f"Investigate why Store {int(lowest_store['store_id'])} trails the stronger locations.")
]
for number, title, action in actions:
    st.markdown(f"**{number}. {title}**\n\n{action}")

st.divider()
st.success("The analysis suggests that the biggest opportunity is not simply generating more orders, but improving the value and profitability of existing demand.")
st.caption("Restaurant Business Analytics • Business Insights")
