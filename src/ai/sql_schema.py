"""
Database schema utilities for InsightAI.

Responsible for inspecting the SQLite database
and generating schema information for the SQL Agent.
"""


def get_database_schema(connection):
    """
    Inspect the SQLite database and return its schema
    as a readable text description.
    """

    cursor = connection.cursor()

    # Get all user-created tables
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)

    tables = cursor.fetchall()

    schema_parts = []

    for (table_name,) in tables:

        schema_parts.append(f"TABLE: {table_name}")

        # Get column information
        cursor.execute(
            f"PRAGMA table_info({table_name})"
        )

        columns = cursor.fetchall()

        for column in columns:

            column_name = column[1]
            data_type = column[2]
            primary_key = column[5]

            column_description = (
                f"  - {column_name} ({data_type})"
            )

            if primary_key:
                column_description += " [PRIMARY KEY]"

            schema_parts.append(column_description)

        # Get foreign-key information
        cursor.execute(
            f"PRAGMA foreign_key_list({table_name})"
        )

        foreign_keys = cursor.fetchall()

        for foreign_key in foreign_keys:

            referenced_table = foreign_key[2]
            from_column = foreign_key[3]
            referenced_column = foreign_key[4]

            schema_parts.append(
                f"  - FOREIGN KEY: "
                f"{from_column} -> "
                f"{referenced_table}.{referenced_column}"
            )

        schema_parts.append("")

    return "\n".join(schema_parts)
