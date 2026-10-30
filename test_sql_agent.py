import sqlite3

from src.ai.sql_agent import run_sql_agent
from src.config import DATABASE_FILE


connection = sqlite3.connect(
    DATABASE_FILE
)

question = "Which customer generated the highest revenue?"

answer = run_sql_agent(
    question,
    connection
)

print("\nQuestion:")
print(question)

print("\nInsightAI Answer:")
print(answer)

connection.close()