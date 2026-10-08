import argparse
import csv
import sqlite3
from pathlib import Path


TABLE_COLUMNS = {
    "customers": (
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "city",
        "province",
        "country",
        "created_timestamp",
        "updated_timestamp",
        "is_active",
    ),
    "stores": (
        "store_id",
        "store_name",
        "city",
        "province",
        "country",
        "created_timestamp",
        "updated_timestamp",
        "is_active",
    ),
    "products": (
        "product_id",
        "product_name",
        "category",
        "brand",
        "price",
        "created_timestamp",
        "updated_timestamp",
        "is_active",
    ),
    "employees": (
        "employee_id",
        "store_id",
        "first_name",
        "last_name",
        "email",
        "job_title",
        "salary",
        "created_timestamp",
        "updated_timestamp",
        "is_active",
    ),
    "orders": (
        "order_id",
        "customer_id",
        "store_id",
        "order_timestamp",
        "payment_method",
        "order_status",
        "total_amount",
        "created_timestamp",
        "updated_timestamp",
        "is_active",
    ),
    "order_items": (
        "order_item_id",
        "order_id",
        "product_id",
        "quantity",
        "unit_price",
        "line_amount",
        "created_timestamp",
        "updated_timestamp",
        "is_active",
    ),
}


def create_database(database_path: Path, replace: bool = False) -> dict[str, int]:
    project_root = Path(__file__).resolve().parents[2]
    data_directory = project_root / "walmart_dataset" / "data"
    schema_path = project_root / "walmart_dataset" / "ddl" / "walmart_schema.sql"
    if not schema_path.is_file():
        raise FileNotFoundError(f"Database schema not found: {schema_path}")

    database_path = database_path.expanduser().resolve()
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path)
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        existing_tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        managed_tables = existing_tables.intersection(TABLE_COLUMNS)
        if managed_tables and not replace:
            names = ", ".join(sorted(managed_tables))
            raise FileExistsError(
                f"{database_path} already contains Walmart tables ({names}); "
                "use --replace to rebuild them"
            )

        statements = ["BEGIN IMMEDIATE;"]
        if replace:
            for table in (
                "order_items",
                "orders",
                "employees",
                "products",
                "stores",
                "customers",
            ):
                statements.append(f"DROP TABLE IF EXISTS {table};")
        statements.append(schema_path.read_text(encoding="utf-8"))
        connection.executescript("\n".join(statements))

        row_counts: dict[str, int] = {}
        for table, columns in TABLE_COLUMNS.items():
            csv_path = data_directory / f"{table}.csv"
            if not csv_path.is_file():
                raise FileNotFoundError(f"CSV data file not found: {csv_path}")

            placeholders = ", ".join("?" for _ in columns)
            column_names = ", ".join(columns)
            insert_sql = (
                f"INSERT INTO {table} ({column_names}) "
                f"VALUES ({placeholders})"
            )

            with csv_path.open(encoding="utf-8-sig", newline="") as csv_file:
                reader = csv.DictReader(csv_file)
                if reader.fieldnames != list(columns):
                    raise ValueError(
                        f"Unexpected columns in {csv_path}: {reader.fieldnames}"
                    )

                def values():
                    for line_number, row in enumerate(reader, start=2):
                        if None in row or any(
                            row.get(column) is None for column in columns
                        ):
                            raise ValueError(
                                f"Malformed CSV row at {csv_path}:{line_number}"
                            )
                        yield tuple(
                            row[column] if row[column] != "" else None
                            for column in columns
                        )

                cursor = connection.executemany(insert_sql, values())
                row_counts[table] = cursor.rowcount

        connection.commit()
        return row_counts
    except (OSError, csv.Error, sqlite3.Error, ValueError):
        connection.rollback()
        raise
    finally:
        connection.close()


def main() -> None:
    project_root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(
        description="Create a local SQLite database from the Walmart CSV dataset."
    )
    parser.add_argument(
        "--database",
        type=Path,
        default=project_root / "walmart.db",
        metavar="PATH",
        help="database file path (default: ./walmart.db)",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="replace existing Walmart tables in the target database",
    )
    args = parser.parse_args()

    try:
        row_counts = create_database(args.database, replace=args.replace)
    except (OSError, csv.Error, sqlite3.Error, ValueError) as error:
        parser.error(str(error))

    print(f"Created SQLite database at {args.database.expanduser().resolve()}")
    for table, count in row_counts.items():
        print(f"  {table}: {count} rows")
