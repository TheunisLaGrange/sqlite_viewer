import csv
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from data_access.db_service import SQLiteService
from gui.ui_components.main_layout import ViewerLayout

class SQLiteViewerWindow:
    """Coordinates UI interactions, SQLiteService queries, and CSV exports."""

    def __init__(self, root: tk.Tk, default_db: Path | None = None) -> None:
        self.service: SQLiteService | None = None
        self.current_columns: list[str] = []
        self.current_rows: list[tuple] = []

        self.ui = ViewerLayout(
            root=root,
            on_open=self.open_file_dialog,
            on_refresh=self.refresh_database,
            on_export=self.export_csv,
            on_table_select=self.on_table_select,
            on_run_sql=self.run_custom_query,
        )

        if default_db and default_db.exists():
            self.load_database(default_db)

    def open_file_dialog(self) -> None:
        selected = filedialog.askopenfilename(
            title="Select SQLite Database",
            filetypes=[
                ("SQLite Databases", "*.db *.sqlite *.sqlite3"),
                ("All Files", "*.*"),
            ],
        )
        if selected:
            self.load_database(Path(selected))

    def load_database(self, path: Path) -> None:
        if not path.exists():
            messagebox.showerror("File Missing", f"Database not found:\n{path}")
            return

        self.service = SQLiteService(path)
        self.ui.set_db_title(f"DB: {path.name}")
        self.refresh_database()

    def refresh_database(self) -> None:
        if not self.service:
            return

        try:
            tables_info = self.service.get_tables_with_counts()
            formatted_tables = [f"{tbl} ({count})" for tbl, count in tables_info]
            self.ui.set_tables(formatted_tables)
            self.ui.set_schema_tokens(self.service.get_schema_tokens())
            self.ui.set_tickers(self.service.get_distinct_tickers())
            self.ui.set_status(
                f"Loaded {len(tables_info)} tables from {self.service.db_path}"
            )
            if tables_info:
                self.on_table_select()
        except Exception as exc:
            messagebox.showerror("Database Error", f"Failed to read database:\n{exc}")

    def on_table_select(self) -> None:
        table_name = self.ui.get_selected_table()
        if not table_name:
            return
        sql = f'SELECT * FROM "{table_name}" ORDER BY 1 DESC LIMIT 500;'
        self.ui.set_query_text(sql)
        self.execute_query(sql)

    def run_custom_query(self) -> None:
        sql = self.ui.get_query_text()
        if sql:
            self.execute_query(sql)

    def execute_query(self, sql: str) -> None:
        if not self.service:
            messagebox.showwarning(
                "No Database", "Please open a SQLite database first."
            )
            return

        try:
            res = self.service.execute_query(sql)
            if res["status"] == "NON_QUERY":
                self.ui.set_status("Statement executed successfully.")
                self.refresh_database()
                return

            self.current_columns = res["columns"]
            self.current_rows = res["rows"]
            self.ui.populate_grid(self.current_columns, self.current_rows)
            self.ui.set_status(f"Returned {res['row_count']} rows.")
        except Exception as exc:
            messagebox.showerror("SQL Error", f"Query failed:\n{exc}")

    def export_csv(self) -> None:
        if not self.current_columns:
            messagebox.showinfo(
                "Nothing to Export", "Run a query or select a table first."
            )
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Export Current View",
        )
        if not save_path:
            return

        try:
            with open(save_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.current_columns)
                writer.writerows(self.current_rows)
            self.ui.set_status(
                f"Exported {len(self.current_rows)} rows to {save_path}"
            )
        except Exception as exc:
            messagebox.showerror("Export Error", f"Failed to write CSV:\n{exc}")
