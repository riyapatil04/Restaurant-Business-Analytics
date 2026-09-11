PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS restaurants (
    restaurant_id INTEGER PRIMARY KEY,
    restaurant_name TEXT NOT NULL,
    location TEXT
);

CREATE TABLE IF NOT EXISTS menu_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    menu_item TEXT NOT NULL UNIQUE,
    category TEXT,
    selling_price REAL,
    ingredient_cost REAL,
    packaging_cost REAL,
    labor_cost REAL,
    total_cogs REAL,
    food_cost_pct REAL,
    supplier TEXT,
    last_updated TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    restaurant_id INTEGER NOT NULL,
    transaction_datetime TEXT,
    business_day TEXT,
    daypart TEXT,
    service_mode TEXT,
    payment_type TEXT,

    FOREIGN KEY (restaurant_id)
        REFERENCES restaurants(restaurant_id)
);

CREATE TABLE IF NOT EXISTS order_items (
    order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id TEXT NOT NULL,
    item_id INTEGER NOT NULL,
    modifier TEXT,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL CHECK (unit_price >= 0),
    discount REAL DEFAULT 0 CHECK (discount >= 0),
    tax REAL DEFAULT 0 CHECK (tax >= 0),
    total_amount REAL,

    FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    FOREIGN KEY (item_id)
        REFERENCES menu_items(item_id)
);

CREATE INDEX IF NOT EXISTS idx_orders_restaurant
ON orders(restaurant_id);

CREATE INDEX IF NOT EXISTS idx_orders_business_day
ON orders(business_day);

CREATE INDEX IF NOT EXISTS idx_order_items_order
ON order_items(order_id);

CREATE INDEX IF NOT EXISTS idx_order_items_item
ON order_items(item_id);