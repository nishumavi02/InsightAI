CREATE TABLE customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    age INTEGER CHECK (age >= 0),
    gender TEXT,
    city TEXT,
    state TEXT
);

CREATE TABLE products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL CHECK (price >= 0),
    supplier_id TEXT,
    inventory_level INTEGER CHECK (inventory_level >= 0)
);