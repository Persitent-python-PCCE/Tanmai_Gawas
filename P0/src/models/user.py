class User:
    def __init__(self, user_id, full_name, role, email, phone=None, address=None, date_of_birth=None):
        self.user_id = user_id
        self._full_name = full_name
        self.role = role
        self.email = email
        self.phone = phone
        self.address = address
        self.date_of_birth = date_of_birth

    @property
    def full_name(self):
        return self._full_name

    def get_dashboard_menu(self):
        """Polymorphic method returning options list based on user subclass."""
        raise NotImplementedError("Subclasses must implement this method")