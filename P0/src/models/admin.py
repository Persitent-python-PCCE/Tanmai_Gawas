from src.models.user import User

class Admin(User):
    def __init__(self, user_id, full_name, email, phone=None, address=None, date_of_birth=None):
        super().__init__(user_id, full_name, "admin", email, phone, address, date_of_birth)

    def get_dashboard_menu(self):
        return [
            "View All Products",
            "Search / Filter Products",
            "Add Product",
            "Update Product",
            "Delete Product",
            "Bulk Upload Products",
            "View All Orders",
            "Search / Filter Orders",
            "Approve Order",
            "Export Database (Backup)",
            "Logout"
        ]