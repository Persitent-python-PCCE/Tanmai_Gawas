from src.utils.backup import backup_table_to_csv, backup_table_to_json
from src.utils.logger import log_action

class CustomerService:
    def __init__(self, customer_dao):
        self.customer_dao = customer_dao

    def run_backup(self, format_type="csv"):
        tables = ["users", "products", "orders", "order_items"]
        paths = []
        for table in tables:
            if format_type.lower() == "csv":
                p = backup_table_to_csv(table)
            else:
                p = backup_table_to_json(table)
            paths.append(p)
        log_action(f"Backup executed successfully for tables: {', '.join(tables)} in '{format_type}' format.")
        return paths

    def update_user(self, user_id, phone, address, date_of_birth):
        existing_user = self.customer_dao.get_by_id(user_id)

        if not existing_user:
            log_action(f"Failed to update profile: User ID #{user_id} not found.", "warning")
            raise ValueError("User not found.")

        self.customer_dao.update_profile(
            user_id,
            phone,
            address,
            date_of_birth
        )
        log_action(f"User ID #{user_id} successfully updated their profile.")
