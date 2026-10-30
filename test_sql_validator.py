from src.ai.sql_validator import validate_sql


test_queries = [
    (
        "SELECT * FROM customers;",
        "SAFE SELECT"
    ),
    (
        """
        SELECT
            c.customer_name
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        GROUP BY c.customer_id, c.customer_name
        ORDER BY SUM(o.total_amount) DESC
        LIMIT 1;
        """,
        "SAFE ANALYTICS QUERY"
    ),
    (
        """
        WITH customer_revenue AS (
            SELECT
                customer_id,
                SUM(total_amount) AS revenue
            FROM orders
            GROUP BY customer_id
        )
        SELECT *
        FROM customer_revenue;
        """,
        "SAFE CTE QUERY"
    ),
    (
        "DROP TABLE customers;",
        "DANGEROUS DROP"
    ),
    (
        "DELETE FROM customers;",
        "DANGEROUS DELETE"
    ),
    (
        "UPDATE customers SET city = 'Delhi';",
        "DANGEROUS UPDATE"
    ),
    (
        "INSERT INTO customers VALUES ('C999', 'Test', 20, 'M', 'Delhi', 'UP');",
        "DANGEROUS INSERT"
    ),
]


for query, description in test_queries:

    is_valid, message = validate_sql(query)

    print("\n-----------------------------")
    print(description)
    print("-----------------------------")
    print("Valid:", is_valid)
    print("Message:", message)