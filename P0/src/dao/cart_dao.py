from config.database import execute_query, execute_update
from src.models.cart import Cart

class CartDAO:
    def __init__(self, product_dao):
        self.product_dao = product_dao

    def get_by_user_id(self, user_id):
        cart = Cart()
        rows = execute_query(
            "SELECT product_id, quantity FROM cart_items WHERE user_id = %s",
            (user_id,)
        )
        for row in rows:
            product = self.product_dao.get_by_id(row["product_id"])
            if product:
                cart.add_item(product, row["quantity"])
        return cart

    def save_item(self, user_id, product_id, quantity):
        execute_update(
            """
            INSERT INTO cart_items (user_id, product_id, quantity)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE quantity = %s
            """,
            (user_id, product_id, quantity, quantity)
        )

    def delete_item(self, user_id, product_id):
        execute_update(
            "DELETE FROM cart_items WHERE user_id = %s AND product_id = %s",
            (user_id, product_id)
        )

    def clear(self, user_id):
        execute_update(
            "DELETE FROM cart_items WHERE user_id = %s",
            (user_id,)
        )