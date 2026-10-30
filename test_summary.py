import sqlite3

from src.ai.business_context import build_business_context
from src.ai.executive_summary import generate_executive_summary
from src.config import DATABASE_FILE

connection = sqlite3.connect(DATABASE_FILE)

context = build_business_context(connection)

summary = generate_executive_summary(context)

print(summary)

connection.close()