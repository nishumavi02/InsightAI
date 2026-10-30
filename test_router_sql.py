import sqlite3

from src.ai.decision_router import route_question
from src.ai.sql_agent import run_sql_agent
from src.config import DATABASE_FILE


connection = sqlite3.connect(DATABASE_FILE)

question = "Which customer generated the highest revenue?"

route = route_question(question)

print("\n--- ROUTER RESULT ---")
print(route)

if route == "SQL":

    answer = run_sql_agent(
        question,
        connection
    )

    print("\n--- SQL AGENT ANSWER ---")
    print(answer)

else:

    print(
        f"Question was routed to {route}, "
        "so SQL Agent was not executed."
    )

connection.close()