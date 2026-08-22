from pathlib import Path

code = '''
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Operations & Strategy",
    page_icon="\u2699\uFE0F",
    layout="wide"
)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ANALYTICS_PATH = PROJECT_ROOT / "data" / "processed" / "analytics"

@st.cache_data
def load_data():
    store = pd.read_csv(ANALYTICS_PATH / "store_analysis.csv")
    operations_hourly = pd.read_csv(ANALYTICS_PATH / "operations_hourly.csv")
    operations_daypart = pd.read_csv(ANALYTICS_PATH / "operations_daypart.csv")
    operations_weekday = pd.read_csv(ANALYTICS_PATH / "operations_weekday.csv")
    discount = pd.read_csv(ANALYTICS_PATH / "discount_analysis.csv")
    modifier = pd.read_csv(ANALYTICS_PATH / "modifier_analysis.csv")
    strategic = pd.read_csv(ANALYTICS_PATH / "strategic" / "strategic_menu_analysis.csv")
    return store, operations_hourly, operations_daypart, operations_weekday, discount, modifier, strategic

store, operations_hourly, operations_daypart, operations_weekday, discount, modifier, strategic = load_data()

st.title("⚙️ Operations & Strategy")
st.caption("Operational performance, promotions and strategic opportunities")
st.divider()

st.subheader("🏪 Store Performance")
fig_store = px.bar(
    store.sort_values("revenue"),
    x="revenue", y="store_id", orientation="h", text="revenue",
    labels={"revenue": "Revenue ($)", "store_id": "Store"}
)
fig_store.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
fig_store.update_layout(height=450, margin=dict(l=20, r=60, t=20, b=20))
st.plotly_chart(fig_store, width="stretch")

best_store = store.loc[store["revenue"].idxmax()]
lowest_store = store.loc[store["revenue"].idxmin()]
c1, c2 = st.columns(2)
with c1:
    st.success(f"**Top Store**\\n\\nStore **{int(best_store['store_id'])}**\\n\\nRevenue: ****\\n\\nAOV: ****")
with c2:
    st.warning(f"**Lowest Revenue Store**\\n\\nStore **{int(lowest_store['store_id'])}**\\n\\nRevenue: ****\\n\\nAOV: ****")

st.divider()
st.subheader("⏰ Peak Operating Hours")
fig_hour = px.bar(
    operations_hourly.sort_values("revenue"),
    x="revenue", y="hour", orientation="h", text="revenue",
    labels={"revenue": "Revenue ($)", "hour": "Hour"}
)
fig_hour.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
fig_hour.update_layout(height=450, margin=dict(l=20, r=60, t=20, b=20))
st.plotly_chart(fig_hour, width="stretch")
peak_hour = operations_hourly.loc[operations_hourly["revenue"].idxmax()]
st.info(f"Peak revenue hour is **{int(peak_hour['hour'])}:00**, generating ****.")

st.divider()
c1, c2 = st.columns(2)
with c1:
    st.subheader("🕐 Daypart Performance")
    fig = px.bar(
        operations_daypart.sort_values("revenue"),
        x="revenue", y="daypart", orientation="h", text="revenue",
        labels={"revenue": "Revenue ($)", "daypart": "Daypart"}
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_layout(height=400, margin=dict(l=20, r=60, t=20, b=20))
    st.plotly_chart(fig, width="stretch")
with c2:
    st.subheader("📅 Weekday Performance")
    fig = px.bar(
        operations_weekday.sort_values("revenue"),
        x="revenue", y="day_name", orientation="h", text="revenue",
        labels={"revenue": "Revenue ($)", "day_name": "Day"}
    )
    fig.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig.update_layout(height=400, margin=dict(l=20, r=60, t=20, b=20))
    st.plotly_chart(fig, width="stretch")

st.divider()
st.subheader("🎯 Discount Strategy")
fig = px.bar(
    discount,
    x="discount_status", y="avg_order_value", text="avg_order_value",
    labels={"discount_status": "", "avg_order_value": "Average Order Value ($)"}
)
fig.update_traces(texttemplate="$%{text:.2f}", textposition="outside")
fig.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig, width="stretch")
discounted = discount[discount["discount_status"] == "Discounted"].iloc[0]
normal = discount[discount["discount_status"] == "No Discount"].iloc[0]
aov_diff = ((discounted["avg_order_value"] / normal["avg_order_value"]) - 1) * 100
st.warning(f"Discounted orders have an AOV of **** versus **** for normal orders. That is a **{abs(aov_diff):.1f}% lower AOV** for discounted orders.")

st.divider()
st.subheader("🧩 Modifier Usage")
mod_disp = modifier[modifier["modifier_clean"] != "No Modifier"].copy()
mod_disp = mod_disp.sort_values("orders", ascending=False).head(12)
fig = px.bar(
    mod_disp.sort_values("orders"),
    x="orders", y="modifier_clean", orientation="h", text="usage_share_pct",
    labels={"orders": "Orders", "modifier_clean": "Modifier"}
)
fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
fig.update_layout(height=500, margin=dict(l=20, r=60, t=20, b=20))
st.plotly_chart(fig, width="stretch")
top_mod = mod_disp.iloc[0]
st.info(f"Most-used modifier: **{top_mod['modifier_clean']}**, appearing in **{int(top_mod['orders'])} orders**.")

st.divider()
st.subheader("🎯 Strategic Menu Actions")
if "strategic_action" in strategic.columns:
    pr = strategic[strategic["strategic_action"].notna()].sort_values("revenue", ascending=False).head(10)
    st.dataframe(pr[["menu_item","menu_classification","strategic_action","revenue","profit_margin_pct"]], width="stretch", hide_index=True)

st.divider()
st.subheader("💡 Management Recommendations")
st.markdown("""
**1. Protect peak periods**  
Lunch and dinner generate the majority of revenue, so staffing and inventory should be optimized around these periods.

**2. Investigate low-performing stores**  
Lower-revenue stores should be compared against stronger stores to identify differences in traffic, service mix and product demand.

**3. Review discount effectiveness**  
Discounted orders have lower AOV, suggesting promotions should be evaluated based on incremental revenue rather than order volume alone.

**4. Increase modifier opportunities**  
Frequently used modifiers can be incorporated into upselling and customization strategies.

**5. Improve high-volume, lower-margin menu items**  
Problem Children should be reviewed for pricing, ingredient costs, portion sizes or recipe optimization.
""")

st.divider()
st.caption("Operations & Strategy • Restaurant Business Analytics")
'''

Path("dashboard/pages/4_Operations_Strategy.py").write_text(code.strip(), encoding="utf-8")
print("Created 4_Operations_Strategy.py")
