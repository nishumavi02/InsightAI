import sqlite3

from src.ai.sql_executor import execute_sql
from src.config import DATABASE_FILE


connection = sqlite3.connect(DATABASE_FILE)


sql = """
SELECT
    c.customer_name,
    c.city,
    ROUND(SUM(o.total_amount), 2) AS total_revenue
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.customer_name,
    c.city
ORDER BY total_revenue DESC
LIMIT 5;
"""


result = execute_sql(connection, sql)


print("\nTop 5 Customers by Revenue")
print("----------------------------")
print(result)


connection.close()