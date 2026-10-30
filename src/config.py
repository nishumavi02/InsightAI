"""
InsightAI Configuration Module

Central configuration for paths, database locations, models, and system parameters.
"""

from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data paths
DATA_DIR = PROJECT_ROOT / "data"
DOCUMENTS_DIR = DATA_DIR / "documents"
CUSTOMERS_FILE = DATA_DIR / "customers.csv"
PRODUCTS_FILE = DATA_DIR / "products.csv"
ORDERS_FILE = DATA_DIR / "orders.csv"

# Database paths
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_FILE = DATABASE_DIR / "insightai.db"
SCHEMA_FILE = DATABASE_DIR / "schema.sql"

# AI / ML Defaults
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
DEFAULT_SIMILARITY_THRESHOLD = 0.35
DEFAULT_FORECAST_HORIZON = 3  # Months ahead

# Ensure database directory exists
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
