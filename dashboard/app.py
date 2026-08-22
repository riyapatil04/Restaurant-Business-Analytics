import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Restaurant Business Analytics",
    page_icon="🍔",
    layout="wide"
)


# ============================================================
# PATH CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ANALYTICS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "analytics"
    / "dashboard"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    kpis = pd.read_csv(
        ANALYTICS_PATH / "dashboard_kpis.csv"
    )

    monthly = pd.read_csv(
        ANALYTICS_PATH / "dashboard_monthly_trend.csv"
    )

    category = pd.read_csv(
        ANALYTICS_PATH / "dashboard_category_performance.csv"
    )

    daypart = pd.read_csv(
        ANALYTICS_PATH / "dashboard_daypart.csv"
    )

    return kpis, monthly, category, daypart


kpis, monthly, category, daypart = load_data()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🍔 Restaurant Analytics")

st.sidebar.markdown(
    """
    ### Navigation

    **Executive Dashboard**

    More analysis pages will be added next.
    """
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "Restaurant Business Analytics Project"
)


# ============================================================
# TITLE
# ============================================================

st.title("🍔 Restaurant Business Analytics")

st.markdown(
    "### Executive Performance Dashboard"
)

st.markdown(
    "A data-driven overview of restaurant sales, profitability and operational performance."
)


# ============================================================
# KPI SECTION
# ============================================================

st.markdown("---")

st.subheader("📊 Key Performance Indicators")


# Convert KPI dataset into dictionary
kpi_dict = dict(
    zip(kpis["metric"], kpis["value"])
)


# Extract KPI values
revenue = kpi_dict.get("Total Revenue", 0)
gross_profit = kpi_dict.get("Gross Profit", 0)
gross_margin = kpi_dict.get("Gross Margin", 0)
orders = kpi_dict.get("Total Orders", 0)
units = kpi_dict.get("Total Units Sold", 0)
aov = kpi_dict.get("Average Order Value", 0)


# Display KPI cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Revenue",
        f"${revenue:,.2f}"
    )

with col2:
    st.metric(
        "Gross Profit",
        f"${gross_profit:,.2f}"
    )

with col3:
    st.metric(
        "Gross Margin",
        f"{gross_margin:.2f}%"
    )


col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Total Orders",
        f"{orders:,.0f}"
    )

with col5:
    st.metric(
        "Units Sold",
        f"{units:,.0f}"
    )

with col6:
    st.metric(
        "Average Order Value",
        f"${aov:.2f}"
    )


# ============================================================
# MONTHLY SALES TREND
# ============================================================

st.markdown("---")

st.subheader("📈 Monthly Revenue Trend")

monthly["period"] = monthly["period"].astype(str)

fig = px.line(
    monthly,
    x="period",
    y="revenue",
    markers=True,
    title="Revenue by Month"
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue ($)",
    hovermode="x unified"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CATEGORY PERFORMANCE
# ============================================================

st.markdown("---")

st.subheader("🍔 Category Performance")

col1, col2 = st.columns(2)

with col1:

    fig_category = px.bar(
        category,
        x="category",
        y="revenue",
        title="Revenue by Category",
        text_auto=".2f"
    )

    fig_category.update_layout(
        xaxis_title="Category",
        yaxis_title="Revenue ($)"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


with col2:

    fig_profit = px.bar(
        category,
        x="category",
        y="gross_profit",
        title="Gross Profit by Category",
        text_auto=".2f"
    )

    fig_profit.update_layout(
        xaxis_title="Category",
        yaxis_title="Gross Profit ($)"
    )

    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )


# ============================================================
# DAYPART PERFORMANCE
# ============================================================

st.markdown("---")

st.subheader("🕐 Revenue by Daypart")

fig_daypart = px.bar(
    daypart,
    x="daypart",
    y="revenue",
    title="Restaurant Revenue by Daypart",
    text_auto=".2f"
)

fig_daypart.update_layout(
    xaxis_title="Daypart",
    yaxis_title="Revenue ($)"
)

st.plotly_chart(
    fig_daypart,
    use_container_width=True
)


# ============================================================
# DATA SUMMARY
# ============================================================

st.markdown("---")

st.subheader("📋 Category Summary")

display_columns = [
    "category",
    "revenue",
    "gross_profit",
    "profit_margin_pct",
    "revenue_share_pct"
]

available_columns = [
    col for col in display_columns
    if col in category.columns
]

st.dataframe(
    category[available_columns],
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Built with Python • Pandas • Plotly • Streamlit"
)