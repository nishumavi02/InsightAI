import sqlite3

from src.config import DATABASE_FILE
from src.ai.ml.ml_data_service import (
    get_monthly_revenue
)


connection = sqlite3.connect(
    DATABASE_FILE
)

dataframe = get_monthly_revenue(
    connection
)

print("\n====================================")
print("ML DATA PREPARATION SUCCESSFUL")
print("====================================\n")

print("Total months:", len(dataframe))

print("\n--- MONTHLY REVENUE DATA ---\n")

print(
    dataframe.to_string(
        index=False
    )
)

print("\n--- DATA TYPES ---\n")

print(dataframe.dtypes)

connection.close()