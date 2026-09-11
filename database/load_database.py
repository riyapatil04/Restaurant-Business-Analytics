from pathlib import Path
import sqlite3
import pandas as pd


# ============================================
# PATHS
# ============================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_PATH = PROJECT_ROOT / "database" / "restaurant.db"

POS_PATH = PROJECT_ROOT / "data" / "processed" / "qsr_pos_enriched.csv"
COGS_PATH = PROJECT_ROOT / "data" / "processed" / "menu_cogs_cleaned.csv"


# ============================================
# LOAD DATA
# ============================================

print("\nLoading source data...")

pos = pd.read_csv(POS_PATH)
cogs = pd.read_csv(COGS_PATH)

print(f"POS rows: {len(pos)}")
print(f"COGS rows: {len(cogs)}")


# ============================================
# CONNECT TO DATABASE
# ============================================

db = sqlite3.connect(DB_PATH)

# Enable foreign-key enforcement
db.execute("PRAGMA foreign_keys = ON")


# ============================================
# CLEAR EXISTING DATA
# ============================================

print("\nClearing existing database data...")

db.execute("DELETE FROM order_items")
db.execute("DELETE FROM orders")
db.execute("DELETE FROM menu_items")
db.execute("DELETE FROM restaurants")


# ============================================
# RESTAURANTS
# ============================================

print("Loading restaurants...")

restaurant_ids = sorted(pos["store_id"].dropna().unique())

restaurants = pd.DataFrame({
    "restaurant_id": restaurant_ids,
    "restaurant_name": [f"Store {int(x)}" for x in restaurant_ids],
    "location": [None] * len(restaurant_ids)
})

restaurants.to_sql(
    "restaurants",
    db,
    if_exists="append",
    index=False
)


# ============================================
# MENU ITEMS
# ============================================

print("Loading menu items...")

menu_columns = [
    "menu_item",
    "category",
    "selling_price",
    "ingredient_cost",
    "packaging_cost",
    "labor_cost",
    "total_cogs",
    "food_cost_pct",
    "supplier",
    "last_updated"
]

cogs[menu_columns].to_sql(
    "menu_items",
    db,
    if_exists="append",
    index=False
)


# ============================================
# CREATE MENU ITEM ID MAPPING
# ============================================

menu_mapping = pd.read_sql_query(
    "SELECT item_id, menu_item FROM menu_items",
    db
)

pos = pos.merge(
    menu_mapping,
    on="menu_item",
    how="left"
)


# ============================================
# ORDERS
# ============================================

print("Loading orders...")

orders = (
    pos[
        [
            "order_id",
            "store_id",
            "transaction_datetime",
            "business_day",
            "daypart",
            "service_mode",
            "payment_type"
        ]
    ]
    .drop_duplicates(subset=["order_id"])
    .rename(columns={"store_id": "restaurant_id"})
)

orders.to_sql(
    "orders",
    db,
    if_exists="append",
    index=False
)


# ============================================
# ORDER ITEMS
# ============================================

print("Loading order items...")

order_items = pos[
    [
        "order_id",
        "item_id",
        "modifier",
        "quantity",
        "unit_price",
        "discount",
        "tax",
        "total_amount"
    ]
].copy()

order_items.to_sql(
    "order_items",
    db,
    if_exists="append",
    index=False
)


# ============================================
# COMMIT
# ============================================

db.commit()


# ============================================
# VERIFY
# ============================================

print("\nDatabase row counts:")

tables = [
    "restaurants",
    "menu_items",
    "orders",
    "order_items"
]

for table in tables:
    count = db.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{table}: {count}")


db.close()

print("\nDatabase loaded successfully.")