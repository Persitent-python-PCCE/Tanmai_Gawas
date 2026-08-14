import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_PORT = int(os.environ.get("DB_PORT"))


def create_database_if_not_exists():
    """Create the target database if it does not already exist."""
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )

        cursor = conn.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"
        )

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Database creation check failed: {e}")
        raise


def get_connection():
    """Create and return a new MySQL connection."""
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )


def execute_query(query, params=None):
    """Execute a SELECT query and return results as a list of dictionaries."""

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        return result

    finally:
        cursor.close()
        conn.close()


def execute_update(query, params=None, commit=True):
    """Execute INSERT, UPDATE, or DELETE query."""

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params or ())

        last_id = cursor.lastrowid
        row_count = cursor.rowcount

        if commit:
            conn.commit()

        return last_id, row_count

    except Exception as e:

        if commit:
            conn.rollback()

        raise e

    finally:
        cursor.close()
        conn.close()


def execute_sql_file(file_path):
    """Read and execute an SQL script."""

    conn = get_connection()
    cursor = conn.cursor()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            sql_script = f.read()

        statements = [
            stmt.strip()
            for stmt in sql_script.split(";")
            if stmt.strip()
        ]

        for stmt in statements:
            cursor.execute(stmt)

        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Error executing SQL file {file_path}: {e}")
        raise

    finally:
        cursor.close()
        conn.close()

def execute_many(query, param_list, commit=True):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("START TRANSACTION")
        cursor.executemany(query, param_list)
        row_count = cursor.rowcount

        if commit:
            conn.commit()

        return row_count

    except Exception as e:
        if commit:
            conn.rollback()
        raise e

    finally:
        cursor.close()
        conn.close()