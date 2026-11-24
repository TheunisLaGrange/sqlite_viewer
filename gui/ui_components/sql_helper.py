import re
import tkinter as tk

SQL_KEYWORDS = [
    "SELECT", "FROM", "WHERE", "GROUP BY", "ORDER BY", "DESC", "ASC",
    "LIMIT", "COUNT(", "DISTINCT", "AVG(", "MIN(", "MAX(", "SUM(",
    "AND", "OR", "LIKE", "IN", "BETWEEN", "AS", "JOIN", "ON",
]

PRESET_QUERIES: dict[str, str] = {
    "Select a Quick Query...": "",
    "Count Unique Tickers": (
        "SELECT COUNT(DISTINCT symbol) AS unique_tickers FROM price_history;"
    ),
    "Latest Run — Screening Summary": (
        "SELECT symbol, name, current_price, trend_signal, stress_score, risk_tier, passed_screen "
        "FROM screening_results WHERE run_id = (SELECT MAX(run_id) FROM scan_runs) "
        "ORDER BY stress_score ASC;"
    ),
    "Latest Run — Days & Date Range per Ticker": (
        "SELECT symbol, COUNT(*) AS days, MIN(trade_date) AS start_dt, MAX(trade_date) AS end_dt "
        "FROM price_history WHERE run_id = (SELECT MAX(run_id) FROM scan_runs) "
        "GROUP BY symbol ORDER BY symbol;"
    ),
    "High-Risk Tickers Only": (
        "SELECT symbol, name, risk_tier, stress_score, risk_flags "
        "FROM screening_results WHERE risk_tier = 'HIGH_RISK' "
        "ORDER BY run_id DESC, symbol ASC;"
    ),
    "Scan Run History": (
        "SELECT * FROM scan_runs ORDER BY run_id DESC;"
    ),
    "MSFT Ticker": (
        "SELECT * FROM price_history WHERE symbol = 'MSFT' ORDER BY trade_date DESC LIMIT 20;"
    ),
}


class SQLAutocompleteBalloon:
    """Floating Tkinter popup balloon that suggests SQL keywords, tables, and columns."""

    def __init__(self, entry: tk.Entry) -> None:
        self.entry = entry
        self.schema_tokens: list[str] = []
        self.popup: tk.Toplevel | None = None
        self.listbox: tk.Listbox | None = None

        self.entry.bind("<KeyRelease>", self._on_key_release, add="+")
        self.entry.bind("<Down>", self._focus_popup, add="+")
        self.entry.bind("<Escape>", lambda _: self.hide(), add="+")
        self.entry.bind("<FocusOut>", lambda _: self.entry.after(150, self._check_focus), add="+")

    def set_schema_tokens(self, tokens: list[str]) -> None:
        self.schema_tokens = tokens

    def _get_current_word(self) -> tuple[str, int]:
        cursor_pos = self.entry.index(tk.INSERT)
        text_before = self.entry.get()[:cursor_pos]
        match = re.search(r"([A-Za-z_][A-Za-z0-9_]*)$", text_before)
        if not match:
            return "", cursor_pos
        return match.group(1), match.start(1)

    def _on_key_release(self, event: tk.Event) -> None:
        if event.keysym in ("Up", "Down", "Return", "Escape", "Tab", "Left", "Right"):
            return

        word, _ = self._get_current_word()
        if len(word) < 1:
            self.hide()
            return

        upper_word = word.upper()
        candidates = [kw for kw in SQL_KEYWORDS if kw.startswith(upper_word)]
        candidates += [
            tok for tok in self.schema_tokens
            if tok.upper().startswith(upper_word) and tok not in candidates
        ]

        if not candidates:
            self.hide()
            return

        self._show(candidates[:8])

    def _show(self, items: list[str]) -> None:
        if self.popup is None or not self.popup.winfo_exists():
            self.popup = tk.Toplevel(self.entry)
            self.popup.wm_overrideredirect(True)
            self.popup.configure(bg="#38bdf8", padx=1, pady=1)

            self.listbox = tk.Listbox(
                self.popup,
                bg="#1e293b",
                fg="#f8fafc",
                selectbackground="#0284c7",
                font=("Consolas", 10),
                borderwidth=0,
                highlightthickness=0,
                activestyle="none",
            )
            self.listbox.pack(fill=tk.BOTH, expand=True)
            self.listbox.bind("<Return>", lambda _: self._accept_selection())
            self.listbox.bind("<Double-Button-1>", lambda _: self._accept_selection())
            self.listbox.bind("<Escape>", lambda _: self.hide())

        assert self.listbox is not None
        self.listbox.delete(0, tk.END)
        for item in items:
            self.listbox.insert(tk.END, item)
        self.listbox.selection_set(0)
        self.listbox.configure(height=min(len(items), 6))

        x = self.entry.winfo_rootx() + 8
        y = self.entry.winfo_rooty() + self.entry.winfo_height() + 2
        self.popup.wm_geometry(f"260x{min(len(items), 6) * 22 + 4}+{x}+{y}")
        self.popup.deiconify()

    def _focus_popup(self, _event: tk.Event) -> str | None:
        if self.popup and self.popup.winfo_exists() and self.listbox:
            self.listbox.focus_set()
            return "break"
        return None

    def _accept_selection(self) -> None:
        if not self.listbox:
            return
        sel = self.listbox.curselection()
        if not sel:
            return
        chosen = self.listbox.get(sel[0])
        _, start_idx = self._get_current_word()
        cursor_pos = self.entry.index(tk.INSERT)

        self.entry.delete(start_idx, cursor_pos)
        self.entry.insert(start_idx, chosen)
        self.entry.focus_set()
        self.hide()

    def _check_focus(self) -> None:
        if not self.popup or not self.popup.winfo_exists():
            return
        focused = self.entry.focus_get()
        if focused not in (self.entry, self.listbox):
            self.hide()

    def hide(self) -> None:
        if self.popup and self.popup.winfo_exists():
            self.popup.destroy()
        self.popup = None
        self.listbox = None
