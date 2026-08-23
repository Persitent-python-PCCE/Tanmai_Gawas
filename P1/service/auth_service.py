# service/auth_service.py
"""Authentication related business logic encapsulated in a service class."""

from werkzeug.security import generate_password_hash, check_password_hash
from dao.user_dao import create_user, get_user_by_email
from utils.logger import log_general_action
from flask_login import logout_user as flask_logout_user


class AuthService:
    """Provides methods for user registration, authentication, token generation, and logout."""

    def register_user(self, data):
        email = data.get('email')
        password = data.get('password')
        role = data.get('role', 'student')
        full_name = data.get('full_name')
        education = data.get('education')
        if not email or not password:
            raise ValueError('Email and password required')
        if not full_name:
            raise ValueError('Full name is required')
        import re
        email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_regex, email):
            raise ValueError('Invalid email format')
        if len(password) < 6:
            raise ValueError('Password must be at least 6 characters')
        if get_user_by_email(email):
            raise ValueError('User already exists')
        password_hash = generate_password_hash(password)
        user = create_user(email=email, password_hash=password_hash, role=role, full_name=full_name, education=education)
        log_general_action(f"[OK] User Registered Successfully with email {email}", "info")
        return user, 'User created'

    def authenticate_user(self, data):
        email = data.get('email')
        password = data.get('password')
        user = get_user_by_email(email)
        if user and check_password_hash(user.password_hash, password):
            log_general_action(f"[OK] User Authenticated Successfully with email {email}", "info")
            return user
        return None

    def generate_token(self, user_dict):
        """Create a JWT for the supplied user dictionary.
        ``user_dict`` must contain ``id`` and ``role`` keys.
        """
        from utils.jwt_util import create_access_token
        user_id = user_dict.get('id')
        role = user_dict.get('role')
        if user_id is None or role is None:
            raise ValueError('User dict must contain id and role for token generation')
        return create_access_token(user_id, role, user_dict.get('email', ''))

    def logout_user(self):
        """Log out the current user using Flask-Login's ``logout_user``.
        This is a thin wrapper so the controller can import ``logout_user``
        from the service layer just like the other auth functions.
        """
        flask_logout_user()
        return True


# Module‑level singleton for easy import
auth_service = AuthService()

# Backward‑compatible functional wrappers
def register_user(*args, **kwargs):
    return auth_service.register_user(*args, **kwargs)

def authenticate_user(*args, **kwargs):
    return auth_service.authenticate_user(*args, **kwargs)

def generate_token(*args, **kwargs):
    return auth_service.generate_token(*args, **kwargs)

def logout_user(*args, **kwargs):
    return auth_service.logout_user(*args, **kwargs)
