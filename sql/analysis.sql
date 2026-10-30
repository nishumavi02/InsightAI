-- Total Revenue

SELECT
    SUM(total_amount) AS total_revenue
FROM orders;

-- Total Orders

SELECT
    COUNT(*) AS total_orders
FROM orders;

-- Average Order Value

SELECT
    ROUND(AVG(total_amount), 2) AS average_order_value
FROM orders;

-- Total Customers

SELECT
    COUNT(*) AS total_customers
FROM customers;

-- Top 10 Customers by Number of Orders

SELECT
    c.customer_name,
    c.city,
    COUNT(*) AS total_orders
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name, c.city
ORDER BY total_orders DESC
LIMIT 10;

-- Top 10 Best-Selling Products

SELECT
    p.product_name,
    p.category,
    SUM(o.quantity) AS units_sold
FROM orders o
JOIN products p
ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY units_sold DESC
LIMIT 10;

-- Top 10 Revenue-Generating Products

SELECT
    p.product_name,
    p.category,
    ROUND(SUM(o.total_amount), 2) AS total_revenue
FROM orders o
JOIN products p
ON o.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
ORDER BY total_revenue DESC
LIMIT 10;

-- Revenue by Category

SELECT
    p.category,
    ROUND(SUM(o.total_amount), 2) AS total_revenue
FROM orders o
JOIN products p
ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- Top Cities by Customer Count

SELECT
    city,
    COUNT(*) AS total_customers
FROM customers
GROUP BY city
ORDER BY total_customers DESC;