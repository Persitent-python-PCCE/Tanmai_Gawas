import hashlib
import hmac
import os
from src.utils.logger import log_action
import re
from datetime import datetime
from src.utils import send_email

class AuthService:
    def __init__(self, customer_dao):
        self.customer_dao = customer_dao

    def hash_password(self, password, salt=None):
        if salt is None:
            salt = os.urandom(16).hex()
        hashed = hashlib.sha256((password + salt).encode("utf-8")).hexdigest()
        return f"{salt}:{hashed}"

    def verify_password(self, password, stored_password_hash):
        if ":" not in stored_password_hash:
            return False
        salt, _ = stored_password_hash.split(":", 1)
        expected = self.hash_password(password, salt)
        return expected == stored_password_hash

    def verify_otp(self, entered_otp, stored_otp_hash):
        try:
            entered_otp = entered_otp.strip()

            if not entered_otp.isdigit():
                return False

            entered_otp_hash = hashlib.sha256(
                entered_otp.encode("utf-8")
            ).hexdigest()

            return hmac.compare_digest(
                entered_otp_hash,
                stored_otp_hash
            )

        except (AttributeError, TypeError):
            return False

    def verify_email(self, email):
        if not email:
            raise ValueError("Email cannot be empty.")
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_pattern, email) is not None
    
    def register_user(self, full_name, password, email, phone, address, date_of_birth, role="customer"):
        if email:
            email = email.strip()

        if date_of_birth:
            date_of_birth = date_of_birth.strip()

        if full_name:
            full_name = full_name.strip()

        if len(password) < 4:
            raise ValueError("Password must be at least 4 characters long.")

        if date_of_birth:
            try:
                dob = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date of birth. Use YYYY-MM-DD format.")

            if dob > datetime.today().date():
                raise ValueError("Date of birth cannot be in the future.")

        if role not in ("customer", "admin"):
            raise ValueError("Invalid user role.")

        existing = self.customer_dao.get_by_email(email)

        if existing:
            log_action(
                f"Registration failed: Email '{email}' already exists.",
                "warning"
            )
            raise ValueError(f"Email '{email}' is already registered.")

        hashed_pw = self.hash_password(password)

        try:
            user_id = self.customer_dao.create(
                full_name,
                hashed_pw,
                role,
                email,
                phone,
                address,
                date_of_birth
            )

            log_action(
                f"User registered successfully: Email='{email}', "
                f"Role='{role}', ID={user_id}"
            )

            return user_id

        except Exception as e:
            log_action(f"Registration error for '{full_name}': {e}", "error")
            raise

    def login_user(self, email, password):
            email = email.strip()
    
            if not email or not password:
                return None
    
            user = self.customer_dao.get_by_email(email)
    
            if not user:
                log_action(
                f"Login failed: User '{email}' not found.",
                "warning")
                return None
    
            if self.verify_password(password, user["password"]):
                log_action(
                f"User login successful: Email='{email}', Role='{user['role']}'"
            )
                return {
                "id": user["id"],
                "full_name": user["full_name"],
                "email":user["email"],
                "role": user["role"],
                "phone": user["phone"],
                "address": user["address"],
                "date_of_birth": user["date_of_birth"]
                }
    
            else:
                log_action(
                    f"Login failed: Invalid password for user '{email}'.",
                    "warning"
                )
                return None