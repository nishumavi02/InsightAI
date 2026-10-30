import sqlite3

from src.ai.ai_service import get_ai_executive_summary
from src.config import DATABASE_FILE

connection = sqlite3.connect(DATABASE_FILE)

summary = get_ai_executive_summary(connection)

print(summary)

connection.close()