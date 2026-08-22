import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Sales Analysis",
    page_icon="📈",
    layout="wide"
)


# ============================================================
# PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

ANALYTICS_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "analytics"
)


DASHBOARD_PATH = ANALYTICS_PATH / "dashboard"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    monthly = pd.read_csv(
        DASHBOARD_PATH / "dashboard_monthly_trend.csv"
    )

    weekday = pd.read_csv(
        ANALYTICS_PATH / "sales_weekday.csv"
    )

    daypart = pd.read_csv(
        DASHBOARD_PATH / "dashboard_daypart.csv"
    )

    operations_hourly = pd.read_csv(
    ANALYTICS_PATH / "operations_hourly.csv"
)

    operations_daypart = pd.read_csv(
        ANALYTICS_PATH / "operations_daypart.csv"
    )

    operations_weekday = pd.read_csv(
        ANALYTICS_PATH / "operations_weekday.csv"
    )

    return monthly, weekday, daypart, operations_hourly, operations_daypart, operations_weekday


monthly, weekday, daypart, operations_hourly, operations_daypart, operations_weekday = load_data()


# ============================================================
# TITLE
# ============================================================

st.title("📈 Sales & Trend Analysis")

st.markdown(
    """
    Detailed analysis of revenue trends, customer activity,
    peak periods and sales performance.
    """
)


# ============================================================
# MONTHLY TREND
# ============================================================

st.markdown("---")

st.subheader("📅 Monthly Revenue Trend")

monthly["period"] = monthly["period"].astype(str)


fig = px.line(
    monthly,
    x="period",
    y="revenue",
    markers=True,
    title="Monthly Revenue"
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
# MONTHLY GROWTH
# ============================================================

st.subheader("📊 Monthly Revenue Growth")

fig_growth = px.bar(
    monthly,
    x="period",
    y="revenue_growth_pct",
    text_auto=".2f",
    title="Month-over-Month Revenue Growth (%)"
)

fig_growth.update_layout(
    xaxis_title="Month",
    yaxis_title="Growth (%)"
)

st.plotly_chart(
    fig_growth,
    use_container_width=True
)


# ============================================================
# TREND TABLE
# ============================================================

st.subheader("📋 Monthly Performance")

monthly_columns = [
    "period",
    "orders",
    "revenue",
    "avg_order_value",
    "revenue_growth_pct",
    "rolling_3m_revenue",
    "revenue_trend"
]

available_columns = [
    col for col in monthly_columns
    if col in monthly.columns
]

st.dataframe(
    monthly[available_columns],
    use_container_width=True,
    hide_index=True
)


# ============================================================
# WEEKDAY ANALYSIS
# ============================================================

st.markdown("---")

st.subheader("📆 Weekday Performance")

col1, col2 = st.columns(2)


with col1:

    fig_weekday_revenue = px.bar(
        weekday,
        x="day_name",
        y="revenue",
        title="Revenue by Weekday",
        text_auto=".2f"
    )

    fig_weekday_revenue.update_layout(
        xaxis_title="Day",
        yaxis_title="Revenue ($)"
    )

    st.plotly_chart(
        fig_weekday_revenue,
        use_container_width=True
    )


with col2:

    fig_weekday_aov = px.bar(
        weekday,
        x="day_name",
        y="avg_order_value",
        title="Average Order Value by Weekday",
        text_auto=".2f"
    )

    fig_weekday_aov.update_layout(
        xaxis_title="Day",
        yaxis_title="Average Order Value ($)"
    )

    st.plotly_chart(
        fig_weekday_aov,
        use_container_width=True
    )


# ============================================================
# DAYPART ANALYSIS
# ============================================================

st.markdown("---")

st.subheader("🕐 Daypart Performance")

col1, col2 = st.columns(2)


with col1:

    fig_daypart_revenue = px.bar(
        daypart,
        x="daypart",
        y="revenue",
        title="Revenue by Daypart",
        text_auto=".2f"
    )

    fig_daypart_revenue.update_layout(
        xaxis_title="Daypart",
        yaxis_title="Revenue ($)"
    )

    st.plotly_chart(
        fig_daypart_revenue,
        use_container_width=True
    )


with col2:

    fig_daypart_aov = px.bar(
        daypart,
        x="daypart",
        y="avg_order_value",
        title="AOV by Daypart",
        text_auto=".2f"
    )

    fig_daypart_aov.update_layout(
        xaxis_title="Daypart",
        yaxis_title="Average Order Value ($)"
    )

    st.plotly_chart(
        fig_daypart_aov,
    use_container_width=True
    )


# ============================================================
# HOURLY PERFORMANCE
# ============================================================

st.markdown("---")

st.subheader("⏰ Hourly Sales Performance")

fig_hour = px.bar(
    operations_hourly,
    x="hour",
    y="revenue",
    title="Revenue by Hour",
    text_auto=".2f"
)

fig_hour.update_layout(
    xaxis_title="Hour of Day",
    yaxis_title="Revenue ($)"
)

st.plotly_chart(
    fig_hour,
    use_container_width=True
)


# ============================================================
# PEAK PERIOD INSIGHTS
# ============================================================

st.subheader("🔥 Peak Period Insights")

highest_hour = operations_hourly.loc[
    operations_hourly["revenue"].idxmax()
]

highest_daypart = daypart.loc[
    daypart["revenue"].idxmax()
]

highest_weekday = weekday.loc[
    weekday["revenue"].idxmax()
]


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Peak Revenue Hour",
        f"{int(highest_hour['hour'])}:00"
    )

    st.caption(
        f"Revenue: ${highest_hour['revenue']:,.2f}"
    )


with col2:

    st.metric(
        "Best Daypart",
        highest_daypart["daypart"]
    )

    st.caption(
        f"Revenue: ${highest_daypart['revenue']:,.2f}"
    )


with col3:

    st.metric(
        "Best Weekday",
        highest_weekday["day_name"]
    )

    st.caption(
        f"Revenue: ${highest_weekday['revenue']:,.2f}"
    )


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.markdown("---")

st.subheader("💡 Business Insights")

best_month = monthly.loc[
    monthly["revenue"].idxmax()
]

worst_month = monthly.loc[
    monthly["revenue"].idxmin()
]

best_weekday = weekday.loc[
    weekday["revenue"].idxmax()
]

best_daypart = daypart.loc[
    daypart["revenue"].idxmax()
]


st.markdown(
    f"""
    **Key findings**

    - Highest monthly revenue: **{best_month['period']}**
      (${best_month['revenue']:,.2f})

    - Lowest monthly revenue: **{worst_month['period']}**
      (${worst_month['revenue']:,.2f})

    - Strongest weekday: **{best_weekday['day_name']}**
      (${best_weekday['revenue']:,.2f})

    - Strongest daypart: **{best_daypart['daypart']}**
      (${best_daypart['revenue']:,.2f})

    - Peak operating hour: **{int(highest_hour['hour'])}:00**
    """
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Sales Analysis • Python • Pandas • Plotly • Streamlit"
)