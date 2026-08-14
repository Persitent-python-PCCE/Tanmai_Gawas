class Product:
    def __init__(self, product_id, name, description, price, stock):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock


class Cart:
    def __init__(self):
        self._items = {}  # Encapsulated state: dictionary mapping product_id -> quantity
        self._products = {}  # Encapsulated state: dictionary mapping product_id -> Product object

    def add_item(self, product, quantity=1):
        """Add item to cart after validating availability."""
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        
        current_qty = self._items.get(product.product_id, 0)
        new_qty = current_qty + quantity
        
        if product.stock < new_qty:
            raise ValueError(
                f"Insufficient stock for '{product.name}'. Available: {product.stock}"
            )
        self._items[product.product_id] = new_qty
        self._products[product.product_id] = product

    def remove_item(self, product_id, quantity=None):
        """Remove item from cart or decrease quantity."""
        if product_id not in self._items:
            raise ValueError("Product not in cart.")
        
        if quantity is None or quantity >= self._items[product_id]:
            del self._items[product_id]
            if product_id in self._products:
                del self._products[product_id]
        else:
            if quantity <= 0:
                raise ValueError("Quantity to remove must be greater than zero.")
            self._items[product_id] -= quantity

    def clear(self):
        """Remove all items from the cart."""
        self._items.clear()
        self._products.clear()

    @property
    def items(self):
        """Encapsulated items getter."""
        return self._items

    def get_total_price(self):
        """Calculate the total price of all items in the cart."""
        total = 0.0
        for pid, qty in self._items.items():
            prod = self._products.get(pid)
            if prod:
                total += float(prod.price) * qty
        return total

    def get_summary(self):
        """Get list of item dictionaries detailing cart contents."""
        summary = []
        for pid, qty in self._items.items():
            prod = self._products.get(pid)
            if prod:
                summary.append({
                    "product": prod,
                    "quantity": qty,
                    "subtotal": float(prod.price) * qty
                })
        return summary


class User:
    def __init__(self, user_id, username, role):
        self.user_id = user_id
        self._username = username  # Encapsulated username
        self.role = role

    @property
    def username(self):
        return self._username

    def get_dashboard_menu(self):
        """Polymorphic method returning options list based on user subclass."""
        raise NotImplementedError("Subclasses must implement this method")


class Customer(User):
    def __init__(self, user_id, username):
        super().__init__(user_id, username, "customer")
        self.cart = Cart()  # Encapsulated Shopping Cart instance

    def get_dashboard_menu(self):
        """Polymorphic implementation of Dashboard Menu options."""
        return [
            "View Products",
            "Add to Cart",
            "Remove from Cart",
            "View Cart Summary",
            "Place Order",
            "View Order History",
            "Logout"
        ]


class Admin(User):
    def __init__(self, user_id, username):
        super().__init__(user_id, username, "admin")

    def get_dashboard_menu(self):
        """Polymorphic implementation of Dashboard Menu options."""
        return [
            "View Products",
            "Add Product",
            "Update Product",
            "Delete Product",
            "View All Orders",
            "Export Database (Backup)",
            "Logout"
        ]
