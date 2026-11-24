# 🗄️ sqlite_viewer

## 📖 Overview
`sqlite_viewer` is a zero-dependency, dark-mode desktop GUI application built with Python and Tkinter for inspecting SQLite databases (`stratarisk_store.db` and general `.db` / `.sqlite` files). It provides table browsing, custom SQL execution with live autocomplete, ticker-based filtering, preset analytical queries, and one-click CSV exporting.

## ✨ Features
- 🔍 **Database Auto-Discovery**: Automatically detects and loads `data\output\stratarisk_store.db` on startup if available, or lets you open any `.db` / `.sqlite` database manually.
- 📈 **Dynamic Ticker Filter**: Reads `DISTINCT symbol` values from `price_history` / `screening_results` and filters the latest 20 days of records upon selection.
- ⚡ **Quick Queries Dropdown**: Includes one-click preset queries for unique ticker counts, latest screening summaries, date ranges per ticker, high-risk flags, and scan run history.
- 💡 **SQL Autocomplete Balloon**: Displays a live floating suggestion popup for SQL keywords, table names, and column names as you type (`Down Arrow` + `Enter` or double-click to insert).
- 📤 **CSV Export**: Exports the currently displayed query or table grid directly to a `.csv` file.
- 🎨 **Modern Dark UI**: Styled with a custom dark-mode TTK theme and clean separation between data access and UI components.

## 📁 Project Structure
```text
sqlite_viewer/
├── data_access/
│   └── db_service.py
├── gui/
│   ├── assets/
│   │   └── app_icon.png
│   ├── ui_components/
│   │   ├── main_layout.py
│   │   ├── sql_helper.py
│   │   └── theme.py
│   └── viewer_window.py
├── .gitignore
├── CHANGELOG.md
├── chat_history.txt
├── LICENSE
├── README.md
├── requirements.txt
└── run_sqlite_viewer.py
```

## ⚙️ Setup & Installation
1. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
2. Install dependencies (uses Python standard library `tkinter` and `sqlite3`; install any optional extras if listed):
   ```powershell
   pip install -r requirements.txt
   ```

## 🚀 Usage
Launch the application from the project root directory:
```powershell
python run_sqlite_viewer.py
```

1. 📂 If `data\output\stratarisk_store.db` exists, it loads automatically; otherwise, use the toolbar to browse and open a SQLite file.
2. 📊 Select a table from the sidebar, choose a preset from **Quick Queries**, filter by a stock **Ticker**, or type a custom SQL statement in the query bar.
3. 💾 Click **Export CSV** to save the active results grid.
