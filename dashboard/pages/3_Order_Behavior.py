import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Customer & Order Behavior",
    page_icon="??",
    layout="wide"
)

# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ANALYTICS_PATH = PROJECT_ROOT / "data" / "processed" / "analytics"

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    orders_detail = pd.read_csv(
        ANALYTICS_PATH / "orders_behavior_detail.csv"
    )

    hourly = pd.read_csv(
        ANALYTICS_PATH / "order_behavior_hourly.csv"
    )

    order_size = pd.read_csv(
        ANALYTICS_PATH / "order_size_analysis.csv"
    )

    service = pd.read_csv(
        ANALYTICS_PATH / "service_mode_analysis.csv"
    )

    payment = pd.read_csv(
        ANALYTICS_PATH / "payment_analysis.csv"
    )

    return orders_detail, hourly, order_size, service, payment


orders_detail, hourly, order_size, service, payment = load_data()
# =========================================================
# HEADER
# =========================================================

st.title("?? Customer & Order Behavior")
st.caption("Understanding order size, basket value and purchasing channels")

st.divider()

# =========================================================
# OVERALL ORDER KPIs
# =========================================================

# Compute overall KPIs from orders_detail
avg_items = orders_detail["items"].mean()
avg_order_value = orders_detail["order_revenue"].mean()
largest_order = orders_detail["items"].max()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average Items / Order",
    f"{avg_items:.2f}"
)

col2.metric(
    "Average Order Value",
    f"${avg_order_value:.2f}"
)

col3.metric(
    "Largest Order",
    f"{int(largest_order)} items"
)

st.divider()

# =========================================================
# ORDER SIZE DISTRIBUTION
# =========================================================

st.subheader("📦 Order Size Distribution")

# order_size is already loaded as a separate DataFrame
# Ensure we use the correct column names
# Expected columns: order_size, orders, items_sold, revenue, avg_order_value, order_share_pct

fig_size = px.bar(
    order_size,
    x="order_size",
    y="orders",
    text="order_share_pct",
    labels={
        "order_size": "Order Size",
        "orders": "Number of Orders"
    }
)

fig_size.update_traces(
    texttemplate="%{text:.1f}%",
    textposition="outside"
)

fig_size.update_layout(
    height=380,
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(
    fig_size,
    use_container_width=True
)

st.info(
    "Most orders contain a single item. "
    "This indicates a potential opportunity for upselling "
    "combos, sides and beverages."
)

# =========================================================
# SERVICE MODE
# =========================================================

st.subheader("?? Order Behavior by Service Mode")

service_display = service[
    service["service_mode"] != "Unknown"
].copy()

left, right = st.columns(2)

with left:

    fig_service = px.bar(
        service_display.sort_values("avg_order_value"),
        x="avg_order_value",
        y="service_mode",
        orientation="h",
        text="avg_order_value",
        labels={
            "avg_order_value": "Average Order Value ($)",
            "service_mode": "Service Mode"
        }
    )

    fig_service.update_traces(
        texttemplate="$%{text:.2f}",
        textposition="outside"
    )

    fig_service.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_service,
        use_container_width=True
    )

with right:

    fig_service_revenue = px.pie(
        service_display,
        names="service_mode",
        values="revenue",
        hole=0.45
    )

    fig_service_revenue.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_service_revenue,
        use_container_width=True
    )

# =========================================================
# PAYMENT BEHAVIOR
# =========================================================

st.subheader("?? Payment Behavior")

payment_display = payment[
    payment["payment_type"] != "Unknown"
].copy()

left, right = st.columns(2)

with left:

    fig_payment = px.bar(
        payment_display.sort_values("orders"),
        x="orders",
        y="payment_type",
        orientation="h",
        text="revenue_share_pct",
        labels={
            "orders": "Orders",
            "payment_type": "Payment Method"
        }
    )

    fig_payment.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig_payment.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_payment,
        use_container_width=True
    )

with right:

    fig_payment_aov = px.bar(
        payment_display.sort_values("avg_order_value"),
        x="avg_order_value",
        y="payment_type",
        orientation="h",
        text="avg_order_value",
        labels={
            "avg_order_value": "AOV ($)",
            "payment_type": "Payment Method"
        }
    )

    fig_payment_aov.update_traces(
        texttemplate="$%{text:.2f}",
        textposition="outside"
    )

    fig_payment_aov.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(
        fig_payment_aov,
        use_container_width=True
    )

# =========================================================
# HOURLY BEHAVIOR
# =========================================================

st.subheader("⏰ Hourly Order Behavior")

# hourly is already loaded from order_behavior_hourly.csv
# Expected columns: hour, orders, items_sold, revenue, avg_order_value, revenue_share_pct

fig_hourly = px.line(
    hourly,
    x="hour",
    y="avg_order_value",
    markers=True,
    labels={
        "hour": "Hour",
        "avg_order_value": "Average Order Value ($)"
    }
)

fig_hourly.update_layout(
    height=380,
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(
    fig_hourly,
    use_container_width=True
)

# =========================================================
# KEY INSIGHTS
# =========================================================

st.subheader("?? Order Behavior Insights")

highest_aov_service = service_display.loc[
    service_display["avg_order_value"].idxmax()
]

highest_aov_payment = payment_display.loc[
    payment_display["avg_order_value"].idxmax()
]

highest_aov_hour = hourly.loc[
    hourly["avg_order_value"].idxmax()
]

col1, col2, col3 = st.columns(3)

with col1:
    st.success(
        f"""
        **Highest Service-Mode AOV**

        {highest_aov_service["service_mode"]}

        **${highest_aov_service["avg_order_value"]:.2f}**
        per order
        """
    )

with col2:
    st.success(
        f"""
        **Highest Payment AOV**

        {highest_aov_payment["payment_type"]}

        **${highest_aov_payment["avg_order_value"]:.2f}**
        per order
        """
    )

with col3:
    st.success(
        f"""
        **Highest Hourly AOV**

        {int(highest_aov_hour["hour"])}:00

        **${highest_aov_hour["avg_order_value"]:.2f}**
        per order
        """
    )

st.divider()

st.caption(
    "Customer-level identification is not available in the POS dataset. "
    "This dashboard therefore analyzes transaction-level order behavior."
)
