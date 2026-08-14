import unittest
from unittest.mock import MagicMock
from src.service.order_service import OrderService
from src.models import Product

class TestOrder(unittest.TestCase):
    def setUp(self):
        self.mock_order_repo = MagicMock()
        self.mock_product_repo = MagicMock()
        self.mock_cart_service = MagicMock()
        self.order_service = OrderService(
            self.mock_order_repo, self.mock_product_repo, self.mock_cart_service
        )
        self.prod1 = Product(product_id=101, name="Laptop", description="High-end laptop", price=1000.0, stock=5)

    def test_place_order_empty_cart(self):
        """Placing an order with an empty cart raises ValueError."""
        self.mock_cart_service.get_cart_summary.return_value = []
        
        with self.assertRaises(ValueError) as ctx:
            self.order_service.place_order(user_id=1, email="tanmaygawas31@gmail.com", full_name="test_customer")
        self.assertIn("Cart is empty", str(ctx.exception))

    def test_place_order_success(self):
        """Test successful order placement clears cart, inserts records, updates stock, and commits."""
        # 1. Setup mock cart contents
        self.mock_cart_service.get_cart_summary.return_value = [{
            "product": self.prod1,
            "quantity": 2,
            "subtotal": 2000.0
        }]
        self.mock_cart_service.get_cart_total.return_value = 2000.0
        
        # 2. Setup mock product database refresh (returns Product object)
        self.mock_product_repo.get_by_id.return_value = Product(
            product_id=101,
            name="Laptop",
            description="High-end laptop",
            price=1000.00,
            stock=5
        )
        
        # 3. Setup mock transaction ID
        self.mock_order_repo.place_order_transaction.return_value = 99
        
        order_id = self.order_service.place_order(user_id=1, email="tanmaygawas31@gmail.com", full_name="test_customer")
        
        self.assertEqual(order_id, 99)
        self.mock_order_repo.place_order_transaction.assert_called_once_with(
            1, 2000.0, [{"product_id": 101, "product_name": "Laptop", "quantity": 2, "price": 1000.0}]
        )
        self.mock_cart_service.clear_cart.assert_called_once_with(1)

    def test_place_order_insufficient_stock_at_checkout(self):
        """Test checkout failure if product stock becomes insufficient before payment."""
        # 1. Setup mock cart contents
        self.mock_cart_service.get_cart_summary.return_value = [{
            "product": self.prod1,
            "quantity": 3,
            "subtotal": 3000.0
        }]
        
        # 2. Mock database refresh returns depleted stock
        self.mock_product_repo.get_by_id.return_value = Product(
            product_id=101,
            name="Laptop",
            description="High-end laptop",
            price=1000.00,
            stock=1  # only 1 left!
        )
        
        with self.assertRaises(ValueError) as ctx:
            self.order_service.place_order(user_id=1, email="tanmaygawas31@gmail.com", full_name="test_customer")
        self.assertIn("Insufficient stock", str(ctx.exception))
        
        # Verify no database transaction was committed
        self.mock_order_repo.place_order_transaction.assert_not_called()
