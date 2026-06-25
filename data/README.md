# `data/` — Database Storage Layer

This directory holds the raw SQLite database files for the application.

---

## 1. Purpose

> Why do we have a data folder?

SQLite is a file-based database engine:
- **Local storage isolation**: Keep data files organized in one directory separate from application code files.
- **Support git-ignore patterns**: Make it easy to git-ignore raw database binaries (`.db`, `.sqlite`) so they are never committed to repositories.

---

## 2. Responsibilities

### What belongs inside `data/`

- SQLite database files (`ecommerce.db`, test databases).
- Local database backup files.

### What does NOT belong inside `data/`

- Python code or configuration settings.

---

## 3. Files

### `ecommerce.db`

- **Purpose**: The SQLite database file storing the products, orders, and order_items tables.
- **When is it called**: Initialized on first startup, read and written to by controllers during API requests.
- **Who calls it**: SQLite library connection handlers.

---

## 4. Request Flow

The data folder acts as the terminal storage repository:

```
Controllers ──► config/database.py ──► data/ecommerce.db ◄── [Data Directory]
```

---

## 5. Beginner Explanation

"If I forget this after six months..."

This folder is the physical filing cabinet. Every time we add a product or order, we write it down on a sheet of paper and place it inside this file box (`ecommerce.db`). Since we don't want to upload our customer records to GitHub, we exclude this cabinet from git tracking using `.gitignore`.

---

## 6. Real-World Analogy

- **`data/`** = The warehouse filing cabinet or vault.

---

## 7. Best Practices

### Do

- Add `data/*.db` to `.gitignore` to ensure production or test data is never committed.
- Keep databases backed up regularly if testing manually.

### Don't

- Never commit raw database files to git.
- Don't read or edit `.db` binary files directly inside code editors.

---

## 8. Interview Questions

1. **Why gitignore SQLite database files?**
   Database files contain dynamic development state, test records, or sensitive records. Committing them creates merge conflicts and leaks local data.
2. **What is SQLite?**
   A self-contained, serverless, zero-configuration SQL database engine that reads and writes directly to local disk files.

---

## 9. Learning Notes

### Current Phase (Phase 1)
- Single SQLite database file.

### Future Evolution
- **Phase 4**: In production, SQLite will be replaced by a server-based relational database like PostgreSQL.

---

## 10. Quick Revision

- `data/` contains SQLite `.db` binaries.
- Kept out of version control via `.gitignore`.
- Created automatically on first API startup.
- Keeps raw data separate from code.
