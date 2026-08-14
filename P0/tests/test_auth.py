import unittest
from unittest.mock import MagicMock
from src.service.auth_service import AuthService

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.auth_service = AuthService(self.mock_repo)

    def test_password_hashing(self):
        """Test password hashing and verification."""
        password = "secretpassword"
        hashed = self.auth_service.hash_password(password)
        
        self.assertIn(":", hashed)
        self.assertTrue(self.auth_service.verify_password(password, hashed))
        self.assertFalse(self.auth_service.verify_password("wrongpassword", hashed))

    def test_register_user_success(self):
        """Test registering a new user successfully."""
        self.mock_repo.get_by_full_name.return_value = None  # Username/FullName not taken
        self.mock_repo.create.return_value = 1  # Mock returning user_id=1
        
        user_id = self.auth_service.register_user(
            full_name="testuser",
            password="password123",
            email="petersath123@gmail.com",
            phone="1234567890",
            address="123 Street",
            date_of_birth="1990-01-01",
            role="customer"
        )
        self.assertEqual(user_id, 1)
        self.mock_repo.create.assert_called_once()

    def test_register_user_success_alt_email(self):
        """Test registering a new user successfully with alternate email."""
        self.mock_repo.get_by_full_name.return_value = None
        self.mock_repo.create.return_value = 2
        
        user_id = self.auth_service.register_user(
            full_name="anotheruser",
            password="password123",
            email="tanmaygawas31@gmail.com",
            phone="0987654321",
            address="456 Avenue",
            date_of_birth="1992-05-15",
            role="customer"
        )
        self.assertEqual(user_id, 2)

    def test_register_duplicate_user(self):
        """Test registering a duplicate username raises ValueError."""
        self.mock_repo.get_by_full_name.return_value = {"id": 1}  # Full name already taken
        
        with self.assertRaises(ValueError) as ctx:
            self.auth_service.register_user(
                full_name="testuser",
                password="password123",
                email="petersath123@gmail.com",
                phone="1234567890",
                address="123 Street",
                date_of_birth="1990-01-01"
            )
        self.assertIn("already taken", str(ctx.exception))

    def test_register_invalid_inputs(self):
        """Test registration constraints on length and empty fields."""
        with self.assertRaises(ValueError):
            self.auth_service.register_user(
                full_name="   ",
                password="password123",
                email="petersath123@gmail.com",
                phone="1234567890",
                address="123 Street",
                date_of_birth="1990-01-01"
            )
        with self.assertRaises(ValueError):
            self.auth_service.register_user(
                full_name="user1",
                password="123",  # Password too short
                email="petersath123@gmail.com",
                phone="1234567890",
                address="123 Street",
                date_of_birth="1990-01-01"
            )

    def test_login_user_success(self):
        """Test successful login returns user details."""
        hashed_pw = self.auth_service.hash_password("mypassword")
        self.mock_repo.get_by_email.return_value = {
            "id": 5,
            "full_name": "someuser",
            "email": "petersath123@gmail.com",
            "password": hashed_pw,
            "role": "customer",
            "phone": "1234567890",
            "address": "123 Street",
            "date_of_birth": "1990-01-01"
        }
        
        user = self.auth_service.login_user("petersath123@gmail.com", "mypassword")
        self.assertIsNotNone(user)
        self.assertEqual(user["id"], 5)
        self.assertEqual(user["full_name"], "someuser")
        self.assertEqual(user["role"], "customer")

    def test_login_user_wrong_password(self):
        """Test login fails with incorrect password."""
        hashed_pw = self.auth_service.hash_password("mypassword")
        self.mock_repo.get_by_email.return_value = {
            "id": 5,
            "full_name": "someuser",
            "email": "petersath123@gmail.com",
            "password": hashed_pw,
            "role": "customer",
            "phone": "1234567890",
            "address": "123 Street",
            "date_of_birth": "1990-01-01"
        }
        
        user = self.auth_service.login_user("petersath123@gmail.com", "wrongpassword")
        self.assertIsNone(user)
