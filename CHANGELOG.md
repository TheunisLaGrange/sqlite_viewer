# 📝 Changelog

All notable changes to **sqlite_viewer** will be documented in this file.

## 🚧 [Unreleased]

## 📅 - 2026-11-24
### ✨ Added
- 🔌 **Data Access Layer (`data_access/db_service.py`)**: Implemented SQLite connection management, table row counts, schema token extraction, and distinct ticker lookups.
- 💡 **SQL Helper & Autocomplete (`gui/ui_components/sql_helper.py`)**: Added preset **Quick Queries** (unique ticker counts, latest screening summaries, ticker date ranges, high-risk flags, and scan run history) and a live floating autocomplete balloon for SQL keywords, tables, and columns.
- 📈 **Dynamic Ticker Dropdown**: Added automatic population of distinct symbols from `price_history` / `screening_results` to filter the latest 20 days of records.
- 📤 **CSV Export & Auto-Discovery**: Added one-click CSV export of the active results grid and automatic startup resolution for `data\output\stratarisk_store.db`.
- 🖼️ **Application Icon**: Added `gui/assets/app_icon.png`.

### 🔄 Changed
- 🏗️ Separated database logic into the `data_access` package and wired UI events through `gui/viewer_window.py`.
- 📚 Updated `README.md` project structure and usage documentation to match the current repository layout.

## 📅 - 2026-11-22
### ✨ Added
- 🌱 Initial project scaffolding and standardized repository files (`LICENSE`, `README.md`, `CHANGELOG.md`, `.gitignore`, `requirements.txt`).
- 🎨 Modular `gui` package structure with dark-mode TTK styling (`theme.py`) and core layout (`main_layout.py`).
