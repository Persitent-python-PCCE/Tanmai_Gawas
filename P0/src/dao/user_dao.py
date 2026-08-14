from config.database import execute_query, execute_update

class CustomerDAO:
    def get_by_full_name(self, full_name):
        results = execute_query("SELECT * FROM users WHERE full_name = %s", (full_name,))
        return results[0] if results else None

    def get_by_email(self, email):
        results = execute_query("SELECT * FROM users WHERE email = %s", (email,))
        return results[0] if results else None

    def get_by_id(self, user_id):
        results = execute_query("SELECT * FROM users WHERE id = %s", (user_id,))
        return results[0] if results else None

    def create(self, full_name, hashed_password, role, email, phone, address, date_of_birth):
        user_id, _ = execute_update(
            """
            INSERT INTO users (full_name, password, role, email, phone, address, date_of_birth)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (full_name, hashed_password, role, email, phone, address, date_of_birth)
        )
        return user_id

    def update_profile(self, user_id, phone, address, date_of_birth):
        execute_update(
            "UPDATE users SET phone = %s, address = %s, date_of_birth = %s WHERE id = %s",
            (phone, address, date_of_birth, user_id)
        )