from tkinter import ttk


def apply_dark_theme(style: ttk.Style) -> None:
    """Applies the dark-mode TTK palette across all viewer widgets."""
    style.theme_use("clam")

    style.configure("TFrame", background="#0f172a")
    style.configure("Card.TFrame", background="#1e293b")
    style.configure(
        "TLabel", background="#0f172a", foreground="#e2e8f0", font=("Segoe UI", 10)
    )
    style.configure(
        "Header.TLabel",
        background="#0f172a",
        foreground="#38bdf8",
        font=("Segoe UI", 13, "bold"),
    )
    style.configure(
        "TButton",
        background="#2563eb",
        foreground="#ffffff",
        font=("Segoe UI", 9, "bold"),
        padding=(10, 5),
    )
    style.map("TButton", background=[("active", "#1d4ed8")])

    style.configure(
        "Treeview",
        background="#1e293b",
        foreground="#f8fafc",
        fieldbackground="#1e293b",
        rowheight=26,
        font=("Consolas", 9),
    )
    style.configure(
        "Treeview.Heading",
        background="#334155",
        foreground="#38bdf8",
        font=("Segoe UI", 9, "bold"),
    )
    style.map("Treeview", background=[("selected", "#0284c7")])
