import tkinter as tk
from pathlib import Path

from gui.viewer_window import SQLiteViewerWindow

def main() -> None:
    viewer_root = Path(__file__).resolve().parent
    # Searches upward for data\output\stratarisk_store.db if present
    default_db = viewer_root.parent.parent / "data" / "output" / "stratarisk_store.db"

    root = tk.Tk()
    SQLiteViewerWindow(root, default_db=default_db if default_db.exists() else None)
    root.mainloop()


if __name__ == "__main__":
    main()
