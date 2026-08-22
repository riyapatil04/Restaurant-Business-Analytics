import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Executive Overview",
    page_icon="??",
    layout="wide"
)

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ANALYTICS_PATH = PROJECT_ROOT / "data" / "processed" / "analytics"

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

@st.cache_data
def load_data():

    profitability = pd.read_csv(
        ANALYTICS_PATH / "profitability_summary.csv"
    )

    category = pd.read_csv(
        ANALYTICS_PATH / "profitability_by_category.csv"
    )

    monthly = pd.read_csv(
        ANALYTICS_PATH / "sales_monthly.csv"
    )

    service = pd.read_csv(
        ANALYTICS_PATH / "service_mode_analysis.csv"
    )

    daypart = pd.read_csv(
        ANALYTICS_PATH / "daypart_analysis.csv"
    )

    store = pd.read_csv(
        ANALYTICS_PATH / "store_analysis.csv"
    )

    return profitability, category, monthly, service, daypart, store


profitability, category, monthly, service, daypart, store = load_data()

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("?? Restaurant Business Analytics")
st.caption("Executive Overview | April�August 2025")

st.divider()

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

# Convert long-format KPIs to a dict: metric -> value
kpi_dict = dict(zip(profitability["metric"], profitability["value"]))

total_revenue = kpi_dict.get("Total Revenue", 0)
total_cogs = kpi_dict.get("Total COGS", 0)
gross_profit = kpi_dict.get("Gross Profit", 0)
gross_margin = kpi_dict.get("Gross Margin %", 0)
orders = kpi_dict.get("Total Orders", 0)
units = kpi_dict.get("Total Units Sold", 0)
aov = kpi_dict.get("Average Order Value", 0)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"${total_revenue:,.2f}"
)

col2.metric(
    "Gross Profit",
    f"${gross_profit:,.2f}"
)

col3.metric(
    "Gross Margin",
    f"{gross_margin:.1f}%"
)

col4.metric(
    "Average Order Value",
    f"${aov:.2f}"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Orders",
    f"{orders:,}"
)

col2.metric(
    "Units Sold",
    f"{units:,}"
)

col3.metric(
    "Total COGS",
    f"${total_cogs:,.2f}"
)

col4.metric(
    "Stores",
    f"{store['store_id'].nunique()}"
)

st.divider()

# ---------------------------------------------------------
# REVENUE TREND
# ---------------------------------------------------------

st.subheader("?? Revenue Trend")

monthly["period"] = (
    monthly["month_name"].astype(str)
    + " "
    + monthly["year"].astype(str)
)

fig = px.line(
    monthly,
    x="period",
    y="revenue",
    markers=True,
    labels={
        "period": "Month",
        "revenue": "Revenue ($)"
    }
)

fig.update_layout(
    height=350,
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------------
# CATEGORY + DAYPART
# ---------------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("?? Revenue by Category")

    fig_category = px.bar(
        category.sort_values(
            "revenue",
            ascending=True
        ),
        x="revenue",
        y="category",
        orientation="h",
        labels={
            "revenue": "Revenue ($)",
            "category": "Category"
        }
    )

    fig_category.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

with right:

    st.subheader("?? Revenue by Daypart")

    fig_daypart = px.bar(
        daypart.sort_values(
            "revenue",
            ascending=True
        ),
        x="revenue",
        y="daypart",
        orientation="h",
        labels={
            "revenue": "Revenue ($)",
            "daypart": "Daypart"
        }
    )

    fig_daypart.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_daypart,
        use_container_width=True
    )

# ---------------------------------------------------------
# SERVICE MODE
# ---------------------------------------------------------

st.subheader("?? Revenue by Service Mode")

service_clean = service[
    service["service_mode"] != "Unknown"
].copy()

fig_service = px.pie(
    service_clean,
    names="service_mode",
    values="revenue",
    hole=0.45
)

fig_service.update_layout(
    height=400,
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(
    fig_service,
    use_container_width=True
)

# ---------------------------------------------------------
# MANAGEMENT INSIGHTS
# ---------------------------------------------------------

st.subheader("?? Management Snapshot")

best_category = category.loc[
    category["revenue"].idxmax()
]

best_daypart = daypart.loc[
    daypart["revenue"].idxmax()
]

best_service = service_clean.loc[
    service_clean["revenue"].idxmax()
]

best_store = store.loc[
    store["revenue"].idxmax()
]

insight1, insight2 = st.columns(2)

with insight1:

    st.info(
        f"""
        **Revenue Leader**

        ?? **{best_category['category']}** is the highest-revenue
        category with **${best_category['revenue']:,.2f}** in revenue.

        The strongest daypart is **{best_daypart['daypart']}**,
        generating **${best_daypart['revenue']:,.2f}**.
        """
    )

with insight2:

    st.success(
        f"""
        **Business Performance**

        ?? **{best_service['service_mode']}** generates the most
        revenue among service modes.

        ?? Store **{int(best_store['store_id'])}** is currently
        the highest-revenue store with
        **${best_store['revenue']:,.2f}**.
        """
    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "Restaurant Business Analytics � Executive Dashboard � "
    "Data-driven decision support"
)
