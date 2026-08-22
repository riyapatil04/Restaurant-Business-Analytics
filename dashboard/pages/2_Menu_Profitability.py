import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Menu & Profitability",
    page_icon="🍔",
    layout="wide"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

ANALYTICS_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "analytics"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    profitability = pd.read_csv(
        ANALYTICS_PATH / "profitability_summary.csv"
    )

    category = pd.read_csv(
        ANALYTICS_PATH / "profitability_by_category.csv"
    )

    menu_cost = pd.read_csv(
        ANALYTICS_PATH / "menu_cost_analysis.csv"
    )

    menu = pd.read_csv(
        ANALYTICS_PATH / "menu_analysis.csv"
    )

    matrix = pd.read_csv(
        ANALYTICS_PATH / "menu_matrix.csv"
    )

    strategic = pd.read_csv(
    ANALYTICS_PATH / "strategic" / "strategic_menu_analysis.csv"
    )

    return (
        profitability,
        category,
        menu_cost,
        menu,
        matrix,
        strategic
    )


(
    profitability,
    category,
    menu_cost,
    menu,
    matrix,
    strategic
) = load_data()


# ============================================================
# HEADER
# ============================================================

st.title("🍔 Menu & Profitability Analysis")

st.markdown(
    """
    Understand which menu items generate revenue, which generate profit,
    and where the restaurant can improve margins.
    """
)

st.divider()


# ============================================================
# KPI SECTION
# ============================================================

st.subheader("💰 Overall Profitability")


# Convert long-format KPIs to a dict: metric -> value
kpi_dict = dict(zip(profitability["metric"], profitability["value"]))

col1, col2, col3, col4, col5 = st.columns(5)


with col1:
    st.metric(
        "Total Revenue",
        f"${kpi_dict.get('Total Revenue', 0):,.2f}"
    )

with col2:
    st.metric(
        "Total COGS",
        f"${kpi_dict.get('Total COGS', 0):,.2f}"
    )

with col3:
    st.metric(
        "Gross Profit",
        f"${kpi_dict.get('Gross Profit', 0):,.2f}"
    )

with col4:
    st.metric(
        "Gross Margin",
        f"{kpi_dict.get('Gross Margin %', 0):.2f}%"
    )

with col5:
    st.metric(
        "Average Order",
        f"${kpi_dict.get('Average Order Value', 0):.2f}"
    )


st.divider()


# ============================================================
# CATEGORY PROFITABILITY
# ============================================================

st.subheader("📊 Category Profitability")

col1, col2 = st.columns(2)


with col1:

    fig = px.bar(
        category.sort_values(
            "gross_profit",
            ascending=True
        ),
        x="gross_profit",
        y="category",
        orientation="h",
        title="Gross Profit by Category",
        labels={
            "gross_profit": "Gross Profit",
            "category": "Category"
        }
    )

    fig.update_layout(
        height=450,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.bar(
        category.sort_values(
            "profit_margin_pct",
            ascending=True
        ),
        x="profit_margin_pct",
        y="category",
        orientation="h",
        title="Profit Margin by Category",
        labels={
            "profit_margin_pct": "Profit Margin (%)",
            "category": "Category"
        }
    )

    fig.update_layout(
        height=450,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.dataframe(
    category,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# MENU PERFORMANCE
# ============================================================

st.subheader("🍟 Menu Item Performance")

col1, col2 = st.columns(2)


with col1:

    top_revenue = menu.sort_values(
        "revenue",
        ascending=False
    ).head(10)

    fig = px.bar(
        top_revenue.sort_values("revenue"),
        x="revenue",
        y="menu_item",
        orientation="h",
        title="Top 10 Menu Items by Revenue",
        labels={
            "revenue": "Revenue",
            "menu_item": "Menu Item"
        }
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    top_profit = menu.sort_values(
        "gross_profit",
        ascending=False
    ).head(10)

    fig = px.bar(
        top_profit.sort_values("gross_profit"),
        x="gross_profit",
        y="menu_item",
        orientation="h",
        title="Top 10 Menu Items by Gross Profit",
        labels={
            "gross_profit": "Gross Profit",
            "menu_item": "Menu Item"
        }
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.divider()


# ============================================================
# MENU PERFORMANCE MATRIX
# ============================================================

st.subheader("🎯 Menu Performance Matrix")

st.markdown(
    """
    Items are classified using sales volume and profitability:

    - ⭐ **Star** → High sales + High profitability
    - ⚠️ **Problem Child** → High sales + Low profitability
    - 💎 **Hidden Gem** → Low sales + High profitability
    - 🐶 **Dog** → Low sales + Low profitability
    """
)


classification_colors = {
    "Star": "Star",
    "Problem Child": "Problem Child",
    "Hidden Gem": "Hidden Gem",
    "Dog": "Dog"
}


fig = px.scatter(
    matrix,
    x="quantity_sold",
    y="profit_margin_pct",
    size="revenue",
    hover_name="menu_item",
    color="menu_classification",
    title="Menu Portfolio Matrix",
    labels={
        "quantity_sold": "Quantity Sold",
        "profit_margin_pct": "Profit Margin (%)",
        "menu_classification": "Classification"
    }
)

fig.update_layout(
    height=600
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CLASSIFICATION SUMMARY
# ============================================================

classification_counts = (
    matrix["menu_classification"]
    .value_counts()
    .reset_index()
)

classification_counts.columns = [
    "classification",
    "count"
]


st.subheader("Menu Portfolio Summary")

col1, col2, col3, col4 = st.columns(4)


counts = dict(
    zip(
        classification_counts["classification"],
        classification_counts["count"]
    )
)


with col1:
    st.metric(
        "⭐ Stars",
        counts.get("Star", 0)
    )


with col2:
    st.metric(
        "⚠️ Problem Children",
        counts.get("Problem Child", 0)
    )


with col3:
    st.metric(
        "💎 Hidden Gems",
        counts.get("Hidden Gem", 0)
    )


with col4:
    st.metric(
        "🐶 Dogs",
        counts.get("Dog", 0)
    )


st.divider()


# ============================================================
# MENU COST ANALYSIS
# ============================================================

st.subheader("💸 Menu Cost Analysis")

col1, col2 = st.columns(2)


with col1:

    high_cost = menu_cost.sort_values(
        "food_cost_pct",
        ascending=False
    ).head(10)

    fig = px.bar(
        high_cost.sort_values("food_cost_pct"),
        x="food_cost_pct",
        y="menu_item",
        orientation="h",
        title="Highest Food-Cost Items",
        labels={
            "food_cost_pct": "Food Cost (%)",
            "menu_item": "Menu Item"
        }
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    fig = px.scatter(
        menu_cost,
        x="food_cost_pct",
        y="profit_margin_pct",
        size="selling_price",
        hover_name="menu_item",
        title="Food Cost vs Profit Margin",
        labels={
            "food_cost_pct": "Food Cost (%)",
            "profit_margin_pct": "Profit Margin (%)"
        }
    )

    fig.update_layout(height=500)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


st.divider()


# ============================================================
# STRATEGIC PRIORITIES
# ============================================================

st.subheader("🚨 Strategic Menu Priorities")

priority_items = strategic.head(10)


st.dataframe(
    priority_items,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.subheader("💡 Business Insights")


top_category = category.loc[
    category["gross_profit"].idxmax()
]

highest_margin_category = category.loc[
    category["profit_margin_pct"].idxmax()
]

highest_cost_item = menu_cost.loc[
    menu_cost["food_cost_pct"].idxmax()
]

top_revenue_item = menu.loc[
    menu["revenue"].idxmax()
]


st.markdown(
    f"""
    **Key findings**

    - 🏆 **{top_category['category']}** generates the highest gross profit
      at **${top_category['gross_profit']:,.2f}**.

    - 📈 **{highest_margin_category['category']}** has the highest category
      profit margin at **{highest_margin_category['profit_margin_pct']:.2f}%**.

    - ⚠️ **{highest_cost_item['menu_item']}** has the highest food-cost
      percentage at **{highest_cost_item['food_cost_pct']:.1f}%**.

    - 💰 **{top_revenue_item['menu_item']}** is the highest-revenue menu item,
      generating **${top_revenue_item['revenue']:,.2f}**.

    - 🎯 The menu matrix can help management decide which products to
      promote, reprice, reformulate, or potentially remove.
    """
)


# ============================================================
# RAW DATA
# ============================================================

with st.expander("🔎 View Menu Analysis Data"):

    st.dataframe(
        menu,
        use_container_width=True,
        hide_index=True
    )