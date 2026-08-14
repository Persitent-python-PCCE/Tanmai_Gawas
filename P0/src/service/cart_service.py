from src.utils.logger import log_action

class CartService:
    def __init__(self, cart_dao, product_dao):
        self.cart_dao = cart_dao
        self.product_dao = product_dao

    def get_user_cart(self, user_id):
        return self.cart_dao.get_by_user_id(user_id)

    def add_to_cart(self, user_id, product, quantity):
        cart = self.get_user_cart(user_id)
        cart.add_item(product, quantity)
        updated_quantity = cart.get_item(product.product_id)
        self.cart_dao.save_item(user_id, product.product_id, updated_quantity)
        log_action(f"User #{user_id} added {quantity} x '{product.name}' (ID: {product.product_id}) to cart.")

    def remove_from_cart(self, user_id, product_id, quantity=None):
        cart = self.get_user_cart(user_id)
        cart.remove_item(product_id, quantity)
        remaining_quantity = cart.get_item(product_id)
        if remaining_quantity is None or remaining_quantity == 0:
            self.cart_dao.delete_item(user_id, product_id)
            log_action(f"User #{user_id} removed product ID {product_id} from cart entirely.")
        else:
            self.cart_dao.save_item(user_id, product_id, remaining_quantity)
            log_action(f"User #{user_id} removed {quantity} quantity of product ID {product_id} from cart. Remaining: {remaining_quantity}")

    def clear_cart(self, user_id):
        self.cart_dao.clear(user_id)
        log_action(f"User #{user_id} cleared their cart.")

    def get_cart_summary(self, user_id):
        cart = self.get_user_cart(user_id)
        return cart.get_summary()

    def get_cart_total(self, user_id):
        cart = self.get_user_cart(user_id)
        return cart.get_total_price()