import sqlite3

from src.config import DATABASE_FILE

from src.ai.ml.ml_agent import (
    run_ml_agent
)


connection = sqlite3.connect(
    DATABASE_FILE
)

answer = run_ml_agent(
    connection
)

print(
    "\n===================================="
)

print(
    "ML AGENT TEST"
)

print(
    "====================================\n"
)

print(answer)

connection.close()