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
        self.mock_cart_service.get_cart_summary.return_value = [{
            "product": self.prod1,
            "quantity": 2,
            "subtotal": 2000.0
        }]
        self.mock_cart_service.get_cart_total.return_value = 2000.0
        
        self.mock_product_repo.get_by_id.return_value = Product(
            product_id=101,
            name="Laptop",
            description="High-end laptop",
            price=1000.00,
            stock=5
        )
        
        self.mock_order_repo.place_order_transaction.return_value = 99
        
        order_id = self.order_service.place_order(user_id=1, email="tanmaygawas31@gmail.com", full_name="test_customer")
        
        self.assertEqual(order_id, 99)
        self.mock_order_repo.place_order_transaction.assert_called_once_with(
            1, 2000.0, [{"product_id": 101, "product_name": "Laptop", "quantity": 2, "price": 1000.0}]
        )
        self.mock_cart_service.clear_cart.assert_called_once_with(1)

    def test_place_order_insufficient_stock_at_checkout(self):
        """Test checkout failure if product stock becomes insufficient before payment."""
        self.mock_cart_service.get_cart_summary.return_value = [{
            "product": self.prod1,
            "quantity": 3,
            "subtotal": 3000.0
        }]
        
        self.mock_product_repo.get_by_id.return_value = Product(
            product_id=101,
            name="Laptop",
            description="High-end laptop",
            price=1000.00,
            stock=1
        )
        
        with self.assertRaises(ValueError) as ctx:
            self.order_service.place_order(user_id=1, email="tanmaygawas31@gmail.com", full_name="test_customer")
        self.assertIn("Insufficient stock", str(ctx.exception))
        
        self.mock_order_repo.place_order_transaction.assert_not_called()

    def test_approve_order_success(self):
        """Test successful order approval."""
        self.mock_order_repo.get_order_by_id.return_value = {"id": 1, "status": "Pending"}
        self.mock_order_repo.update_order_status.return_value = True
        
        res = self.order_service.approve_order(1)
        self.assertTrue(res)
        self.mock_order_repo.update_order_status.assert_called_once_with(1, "Approved")

    def test_approve_order_not_found(self):
        """Test approval fails if order does not exist."""
        self.mock_order_repo.get_order_by_id.return_value = None
        
        with self.assertRaises(ValueError) as ctx:
            self.order_service.approve_order(999)
        self.assertIn("does not exist", str(ctx.exception))

    def test_approve_order_already_approved(self):
        """Test approval fails if order is already approved."""
        self.mock_order_repo.get_order_by_id.return_value = {"id": 1, "status": "Approved"}
        
        with self.assertRaises(ValueError) as ctx:
            self.order_service.approve_order(1)
        self.assertIn("already approved", str(ctx.exception))

    def test_place_order_selective_success(self):
        """Test placing an order with selective items checks out only selected items and calls remove_items_from_cart."""
        prod2 = Product(product_id=102, name="Phone", description="Smartphone", price=500.0, stock=10)
        self.mock_cart_service.get_cart_summary.return_value = [
            {"product": self.prod1, "quantity": 1, "subtotal": 1000.0},
            {"product": prod2, "quantity": 2, "subtotal": 1000.0}
        ]
        self.mock_product_repo.get_by_id.return_value = self.prod1 # for prod1 refresh
        
        self.mock_order_repo.place_order_transaction.return_value = 100
        
        order_id = self.order_service.place_order(user_id=1, email="tanmaygawas31@gmail.com", full_name="test_customer", product_ids=[101])
        
        self.assertEqual(order_id, 100)
        self.mock_order_repo.place_order_transaction.assert_called_once_with(
            1, 1000.0, [{"product_id": 101, "product_name": "Laptop", "quantity": 1, "price": 1000.0}]
        )
        self.mock_cart_service.remove_items_from_cart.assert_called_once_with(1, [101])
        self.mock_cart_service.clear_cart.assert_not_called()
