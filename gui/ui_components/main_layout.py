import tkinter as tk
from tkinter import ttk
from typing import Callable

from gui.ui_components.sql_helper import PRESET_QUERIES, SQLAutocompleteBalloon
from gui.ui_components.theme import apply_dark_theme


class ViewerLayout:
    """Builds and manages all Tkinter widgets for the SQLite Viewer."""

    def __init__(
        self,
        root: tk.Tk,
        on_open: Callable[[], None],
        on_refresh: Callable[[], None],
        on_export: Callable[[], None],
        on_table_select: Callable[[], None],
        on_run_sql: Callable[[], None],
    ) -> None:
        self.root = root
        self.on_run_sql = on_run_sql
        self.root.title("StrataRisk — Standalone SQLite Viewer")
        self.root.geometry("1180x720")
        self.root.configure(bg="#0f172a")

        apply_dark_theme(ttk.Style())

        # Top Toolbar
        top_bar = ttk.Frame(self.root, padding=10)
        top_bar.pack(fill=tk.X)

        ttk.Button(top_bar, text="Open .DB File", command=on_open).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(top_bar, text="Refresh", command=on_refresh).pack(
            side=tk.LEFT, padx=(0, 8)
        )
        ttk.Button(top_bar, text="Export View to CSV", command=on_export).pack(
            side=tk.LEFT, padx=(0, 16)
        )

        self.db_label = ttk.Label(
            top_bar, text="No database loaded", style="Header.TLabel"
        )
        self.db_label.pack(side=tk.LEFT)

        # Split Workspace
        main_pane = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        # Left Sidebar: Table List
        left_frame = ttk.Frame(main_pane, style="Card.TFrame", padding=8)
        main_pane.add(left_frame, weight=1)

        ttk.Label(
            left_frame,
            text="Tables",
            background="#1e293b",
            foreground="#38bdf8",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor=tk.W, pady=(0, 6))

        self.table_listbox = tk.Listbox(
            left_frame,
            bg="#0f172a",
            fg="#f8fafc",
            selectbackground="#0284c7",
            font=("Consolas", 10),
            borderwidth=0,
            highlightthickness=1,
            highlightcolor="#334155",
        )
        self.table_listbox.pack(fill=tk.BOTH, expand=True)
        self.table_listbox.bind("<<ListboxSelect>>", lambda _: on_table_select())

        # Right Workspace: Preset Bar + Query Bar + Data Grid
        right_frame = ttk.Frame(main_pane)
        main_pane.add(right_frame, weight=5)

        # Preset Query Row (No-SQL Buttons/Dropdown)
        # Preset Query Row (Quick Queries + Dynamic Ticker Filter)
        preset_bar = ttk.Frame(right_frame)
        preset_bar.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(preset_bar, text="Quick Queries:").pack(side=tk.LEFT, padx=(0, 8))
        self.preset_var = tk.StringVar(value="Select a Quick Query...")
        preset_combo = ttk.Combobox(
            preset_bar,
            textvariable=self.preset_var,
            values=list(PRESET_QUERIES.keys()),
            state="readonly",
            width=36,
        )
        preset_combo.pack(side=tk.LEFT, padx=(0, 16))
        preset_combo.bind("<<ComboboxSelected>>", self._on_preset_chosen)

        ttk.Label(preset_bar, text="Ticker:").pack(side=tk.LEFT, padx=(0, 8))
        self.ticker_var = tk.StringVar(value="All / Select...")
        self.ticker_combo = ttk.Combobox(
            preset_bar,
            textvariable=self.ticker_var,
            values=[],
            state="readonly",
            width=16,
        )
        self.ticker_combo.pack(side=tk.LEFT)
        self.ticker_combo.bind("<<ComboboxSelected>>", self._on_ticker_chosen)

        # SQL Input Row + Autocomplete Balloon
        query_bar = ttk.Frame(right_frame)
        query_bar.pack(fill=tk.X, pady=(0, 8))

        self.query_entry = tk.Entry(
            query_bar,
            bg="#1e293b",
            fg="#f8fafc",
            insertbackground="#38bdf8",
            font=("Consolas", 10),
            relief=tk.FLAT,
        )
        self.query_entry.pack(
            side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0, 8)
        )
        self.query_entry.bind("<Return>", lambda _: on_run_sql())

        self.autocomplete = SQLAutocompleteBalloon(self.query_entry)

        ttk.Button(query_bar, text="Run SQL", command=on_run_sql).pack(side=tk.LEFT)

        grid_frame = ttk.Frame(right_frame)
        grid_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(grid_frame, show="headings")
        y_scroll = ttk.Scrollbar(
            grid_frame, orient=tk.VERTICAL, command=self.tree.yview
        )
        x_scroll = ttk.Scrollbar(
            grid_frame, orient=tk.HORIZONTAL, command=self.tree.xview
        )
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        grid_frame.rowconfigure(0, weight=1)
        grid_frame.columnconfigure(0, weight=1)

        # Bottom Status Bar
        self.status_label = ttk.Label(
            self.root,
            text="Tip: Type in the SQL bar for autocomplete suggestions (Down Arrow + Enter to accept)",
            padding=(10, 4),
        )
        self.status_label.pack(fill=tk.X)

    def _on_preset_chosen(self, _event: tk.Event) -> None:
        label = self.preset_var.get()
        sql = PRESET_QUERIES.get(label, "")
        if sql:
            self.set_query_text(sql)
            self.on_run_sql()

    def set_schema_tokens(self, tokens: list[str]) -> None:
        self.autocomplete.set_schema_tokens(tokens)

    def set_db_title(self, text: str) -> None:
        self.db_label.config(text=text)

    def set_status(self, text: str) -> None:
        self.status_label.config(text=text)

    def get_query_text(self) -> str:
        return self.query_entry.get().strip()

    def set_query_text(self, sql: str) -> None:
        self.query_entry.delete(0, tk.END)
        self.query_entry.insert(0, sql)

    def set_tables(self, items: list[str]) -> None:
        self.table_listbox.delete(0, tk.END)
        for item in items:
            self.table_listbox.insert(tk.END, item)
        if items:
            self.table_listbox.selection_set(0)

    def get_selected_table(self) -> str | None:
        selection = self.table_listbox.curselection()
        if not selection:
            return None
        raw_label = self.table_listbox.get(selection[0])
        return raw_label.rsplit(" (", 1)[0]

    def populate_grid(self, columns: list[str], rows: list[tuple]) -> None:
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = columns

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor=tk.W)

        for row in rows:
            clean_row = ["" if val is None else str(val) for val in row]
            self.tree.insert("", tk.END, values=clean_row)

    def _on_ticker_chosen(self, _event: tk.Event) -> None:
        symbol = self.ticker_var.get().strip()
        if not symbol or symbol == "All / Select...":
            return
        sql = (
            f"SELECT * FROM price_history WHERE symbol = '{symbol}' "
            "ORDER BY trade_date DESC LIMIT 20;"
        )
        self.set_query_text(sql)
        self.on_run_sql()

    def set_tickers(self, tickers: list[str]) -> None:
        self.ticker_combo["values"] = tickers
        self.ticker_var.set("All / Select...")

