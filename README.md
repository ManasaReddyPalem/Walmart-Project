# Walmart Project

Create a local SQLite database from the Walmart dataset CSV files:

```powershell
uv run walmart-project
```

This creates `walmart.db` in the project root and imports the customers, stores,
products, employees, orders, and order items. The database schema is in
`walmart_dataset/ddl/walmart_schema.sql`; the source CSVs are in
`walmart_dataset/data/`.

To choose another database file:

```powershell
uv run walmart-project --database path\to\walmart.db
```

If that database already has Walmart tables, the command stops rather than
overwriting them. To rebuild those tables from the CSVs:

```powershell
uv run walmart-project --replace
```

SQLite is included with Python, so no extra package or database server is
required. Local `.db`, `.sqlite`, and `.sqlite3` files are ignored by Git; share
the schema and CSV import code on GitHub, not the generated database file unless
you intentionally want to publish its contents. The source CSVs are already in
this repository, so they will also be visible if you make the repository public;
remove or exclude them first if they should remain private.