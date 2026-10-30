import sqlite3

from src.config import DATABASE_FILE

from src.ai.ml.ml_data_service import (
    get_monthly_revenue
)

from src.ai.ml.forecasting_service import (
    forecast_next_month
)


connection = sqlite3.connect(
    DATABASE_FILE
)

monthly_revenue = (
    get_monthly_revenue(
        connection
    )
)

result = forecast_next_month(
    monthly_revenue
)

print(
    "\n===================================="
)

print(
    "FORECAST GENERATED"
)

print(
    "====================================\n"
)

print(
    f"Training months: "
    f"{result['training_points']}"
)

print(
    f"Predicted revenue: "
    f"{result['predicted_revenue']:.2f}"
)

connection.close()