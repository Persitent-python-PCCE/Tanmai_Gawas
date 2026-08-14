import unittest
from src.models import Cart, Product

class TestCart(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()
        self.prod1 = Product(product_id=101, name="Laptop", description="High-end laptop", price=1000.0, stock=5)
        self.prod2 = Product(product_id=102, name="Mouse", description="Wireless mouse", price=50.0, stock=2)

    def test_add_item_success(self):
        """Test successfully adding item to cart."""
        self.cart.add_item(self.prod1, 2)
        self.assertEqual(self.cart.items[101], 2)

    def test_add_item_insufficient_stock(self):
        """Test adding quantity higher than stock raises ValueError."""
        with self.assertRaises(ValueError) as ctx:
            self.cart.add_item(self.prod1, 6)
        self.assertIn("Insufficient stock", str(ctx.exception))

    def test_add_item_invalid_quantity(self):
        """Test adding negative or zero quantity raises ValueError."""
        with self.assertRaises(ValueError):
            self.cart.add_item(self.prod1, 0)
        with self.assertRaises(ValueError):
            self.cart.add_item(self.prod1, -5)

    def test_add_item_cumulative_stock_check(self):
        """Test cumulative additions check overall stock capacity."""
        self.cart.add_item(self.prod2, 1)
        with self.assertRaises(ValueError):
            self.cart.add_item(self.prod2, 2)  # Total in cart would be 3, stock is 2

    def test_remove_item_partial(self):
        """Test decreasing cart quantity of a product."""
        self.cart.add_item(self.prod1, 3)
        self.cart.remove_item(101, 1)
        self.assertEqual(self.cart.items[101], 2)

    def test_remove_item_complete(self):
        """Test removing a product completely from cart."""
        self.cart.add_item(self.prod1, 2)
        self.cart.remove_item(101)  # Leaving quantity None removes all
        self.assertNotIn(101, self.cart.items)

    def test_remove_nonexistent_item(self):
        """Test removing a product not in the cart raises ValueError."""
        with self.assertRaises(ValueError):
            self.cart.remove_item(999)

    def test_get_total_price(self):
        """Test calculation of total cart price."""
        self.cart.add_item(self.prod1, 1)
        self.cart.add_item(self.prod2, 2)
        
        # 1000 * 1 + 50 * 2 = 1100
        self.assertEqual(self.cart.get_total_price(), 1100.0)

    def test_get_summary(self):
        """Test list summary output format of cart items."""
        self.cart.add_item(self.prod1, 2)
        summary = self.cart.get_summary()
        
        self.assertEqual(len(summary), 1)
        self.assertEqual(summary[0]["product"].product_id, 101)
        self.assertEqual(summary[0]["quantity"], 2)
        self.assertEqual(summary[0]["subtotal"], 2000.0)
