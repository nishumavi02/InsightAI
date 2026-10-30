import sqlite3

from src.ai.sql_schema import get_database_schema
from src.config import DATABASE_FILE


connection = sqlite3.connect(DATABASE_FILE)

schema = get_database_schema(connection)

print(schema)

connection.close()