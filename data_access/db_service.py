import sqlite3
from pathlib import Path
from typing import Any


class SQLiteService:
    """Handles read/write SQLite operations and returns structured handshakes."""

    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def get_tables_with_counts(self) -> list[tuple[str, int]]:
        """Returns a list of (table_name, row_count) tuples."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
            )
            tables = [row[0] for row in cur.fetchall()]

            result: list[tuple[str, int]] = []
            for tbl in tables:
                cur.execute(f'SELECT COUNT(*) FROM "{tbl}";')
                row = cur.fetchone()
                count = int(row[0]) if row else 0
                result.append((tbl, count))
            return result

    def execute_query(self, sql: str) -> dict[str, Any]:
        """Executes a SQL statement and returns a structured result dictionary."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(sql)

            if cur.description is None:
                conn.commit()
                return {
                    "status": "NON_QUERY",
                    "columns": [],
                    "rows": [],
                    "row_count": cur.rowcount,
                }

            columns = [desc[0] for desc in cur.description]
            rows = cur.fetchall()
            return {
                "status": "SUCCESS",
                "columns": columns,
                "rows": rows,
                "row_count": len(rows),
            }

    def get_schema_tokens(self) -> list[str]:
        """Returns sorted unique table and column names for SQL autocomplete."""
        tokens: set[str] = set()
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT name FROM sqlite_master "
                "WHERE type='table' AND name NOT LIKE 'sqlite_%';"
            )
            tables = [row[0] for row in cur.fetchall()]
            for tbl in tables:
                tokens.add(tbl)
                cur.execute(f'PRAGMA table_info("{tbl}");')
                for col_info in cur.fetchall():
                    tokens.add(col_info[1])
        return sorted(tokens)

    def get_distinct_tickers(self) -> list[str]:
        """Returns sorted distinct ticker symbols stored in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            for table in ("price_history", "screening_results"):
                cur.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
                    (table,),
                )
                if cur.fetchone():
                    cur.execute(
                        f'SELECT DISTINCT symbol FROM "{table}" '
                        "WHERE symbol IS NOT NULL ORDER BY symbol ASC;"
                    )
                    return [row[0] for row in cur.fetchall()]
        return []

