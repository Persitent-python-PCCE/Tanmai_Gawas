import os
import csv
import json
from datetime import datetime, date
from decimal import Decimal
from config.database import execute_query
from src.utils.logger import log_action

def json_serial(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def backup_table_to_csv(table_name, backup_dir="backups"):
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{table_name}_backup_{timestamp}.csv"
    file_path = os.path.join(backup_dir, file_name)

    try:
        rows = execute_query(f"SELECT * FROM {table_name}")

        if not rows:
            columns_info = execute_query(f"DESCRIBE {table_name}")
            columns = [col['Field'] for col in columns_info]
        else:
            columns = list(rows[0].keys())

        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns)
            writer.writeheader()
            for row in rows:
                formatted_row = {}
                for k, v in row.items():
                    if isinstance(v, Decimal):
                        formatted_row[k] = float(v)
                    elif isinstance(v, (datetime, date)):
                        formatted_row[k] = v.isoformat()
                    else:
                        formatted_row[k] = v
                writer.writerow(formatted_row)

        log_action(f"Successfully backed up table '{table_name}' to CSV: {file_path}")
        return file_path
    except Exception as e:
        log_action(f"Failed to backup table '{table_name}' to CSV: {e}", "error")
        raise e

def backup_table_to_json(table_name, backup_dir="backups"):
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{table_name}_backup_{timestamp}.json"
    file_path = os.path.join(backup_dir, file_name)

    try:
        rows = execute_query(f"SELECT * FROM {table_name}")

        with open(file_path, "w", encoding="utf-8") as jsonfile:
            json.dump(rows, jsonfile, default=json_serial, indent=4)

        log_action(f"Successfully backed up table '{table_name}' to JSON: {file_path}")
        return file_path
    except Exception as e:
        log_action(f"Failed to backup table '{table_name}' to JSON: {e}", "error")
        raise e
