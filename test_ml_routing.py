import sqlite3

from src.config import DATABASE_FILE

from src.ai.agent_orchestrator import (
    run_agent
)


connection = sqlite3.connect(
    DATABASE_FILE
)

question = (
    "Predict next month's revenue"
)

answer = run_agent(
    question,
    connection,
)

print(
    "\n===================================="
)

print(
    "ML ROUTING TEST"
)

print(
    "====================================\n"
)

print("Question:")
print(question)

print("\nAnswer:")
print(answer)

connection.close()