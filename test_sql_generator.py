import sqlite3

from src.config import DATABASE_FILE
from src.ai.sql_schema import get_database_schema
from src.ai.sql_generator import generate_sql


connection = sqlite3.connect(DATABASE_FILE)

schema = get_database_schema(connection)

question = "Which customer generated the highest revenue?"

sql = generate_sql(
    question,
    schema
)

print("\nGenerated SQL:\n")
print(sql)

connection.close()