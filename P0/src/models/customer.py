from src.models.user import User
from src.models.cart import Cart


class Customer(User):
    def __init__(
        self,
        user_id,
        full_name,
        email,
        phone=None,
        address=None,
        date_of_birth=None
    ):
        super().__init__(user_id, full_name, "customer", email, phone, address, date_of_birth)

        self.cart = Cart()

    def get_dashboard_menu(self):
        return [
            "View All Products",
            "Search / Filter Products",
            "Add to Cart",
            "Remove from Cart",
            "View Cart Summary",
            "Place Order",
            "View Order History",
            "Update Profile",
            "Logout"
        ]