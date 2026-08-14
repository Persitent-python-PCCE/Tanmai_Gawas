import unittest
from unittest.mock import MagicMock, mock_open, patch
from src.service.product_service import ProductService

class TestProduct(unittest.TestCase):
    def setUp(self):
        self.mock_product_dao = MagicMock()
        self.product_service = ProductService(self.mock_product_dao)

    def test_add_product_success(self):
        """Test adding a product successfully."""
        self.mock_product_dao.get_by_name.return_value = None
        self.mock_product_dao.create.return_value = 101

        pid = self.product_service.add_product("ProductA", "DescriptionA", 10.0, 5, "AdminUser")
        self.assertEqual(pid, 101)
        self.mock_product_dao.create.assert_called_once_with("ProductA", "DescriptionA", 10.0, 5)

    def test_add_product_already_exists(self):
        """Test adding a product that already exists raises ValueError."""
        self.mock_product_dao.get_by_name.return_value = {"id": 101, "name": "ProductA"}

        with self.assertRaises(ValueError) as ctx:
            self.product_service.add_product("ProductA", "DescriptionA", 10.0, 5, "AdminUser")
        self.assertIn("already exists", str(ctx.exception))

    @patch("builtins.open", new_callable=mock_open, read_data="name,price,stock,description\nLaptop,1200.0,5,High-end laptop\nMouse,25.0,10,Wireless mouse\n")
    def test_bulk_upload_success(self, mock_file):
        """Test bulk upload of products from a CSV file successfully."""
        self.mock_product_dao.get_by_name.return_value = None
        self.mock_product_dao.bulk_create.return_value = 2

        result = self.product_service.bulk_upload("dummy.csv", "AdminUser")

        self.assertEqual(result["inserted"], 2)
        self.assertEqual(len(result["failed"]), 0)
        self.mock_product_dao.bulk_create.assert_called_once_with([
            ("Laptop", "High-end laptop", 1200.0, 5),
            ("Mouse", "Wireless mouse", 25.0, 10)
        ])

    @patch("builtins.open", new_callable=mock_open, read_data="name,price,stock,description\n,1200.0,5,Empty name\nMouse,-5.0,10,Negative price\nKeyboard,50.0,-2,Negative stock\n")
    def test_bulk_upload_with_errors(self, mock_file):
        """Test bulk upload of products with validation failures in some rows."""
        self.mock_product_dao.get_by_name.return_value = None
        self.mock_product_dao.bulk_create.return_value = 0

        result = self.product_service.bulk_upload("dummy.csv", "AdminUser")

        self.assertEqual(result["inserted"], 0)
        self.assertEqual(len(result["failed"]), 3)
        # Ensure errors are correctly captured with line numbers (header is row 1, first data is row 2)
        self.assertEqual(result["failed"][0][0], 2)  # Row 2: name is empty
        self.assertEqual(result["failed"][1][0], 3)  # Row 3: price must be > 0 (it's -5)
        self.assertEqual(result["failed"][2][0], 4)  # Row 4: stock cannot be negative (it's -2)
