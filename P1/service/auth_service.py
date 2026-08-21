# service/auth_service.py

from werkzeug.security import generate_password_hash, check_password_hash
from dao.user_dao import create_user, get_user_by_email
from flask_login import login_user, logout_user

from utils.logger import log_general_action


def register_user(data):
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'student')
    # Basic validation
    if not email or not password:
        raise ValueError('Email and password required')
    # Simple email regex validation
    import re
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, email):
        raise ValueError('Invalid email format')
    if len(password) < 6:
        raise ValueError('Password must be at least 6 characters')
    existing = get_user_by_email(email)
    if existing:
        raise ValueError('User already exists')
    password_hash = generate_password_hash(password)
    user = create_user(email=email, password_hash=password_hash, role=role)
    return user, 'User created'


def authenticate_user(data):
    email = data.get('email')
    password = data.get('password')
    user = get_user_by_email(email)
    if user and check_password_hash(user.password_hash, password):
        log_general_action(f"[OK] User Authenticated Successfully with email {email}", "info")
        return user
    return None


def generate_token(user_dict):
    """Create a JWT for the supplied user dictionary.
    ``user_dict`` must contain ``id`` and ``role`` keys.
    """
    from utils.jwt_util import create_access_token
    user_id = user_dict.get('id')
    role = user_dict.get('role')
    if user_id is None or role is None:
        raise ValueError('User dict must contain id and role for token generation')
    return create_access_token(user_id, role, user_dict.get('email', ''))
