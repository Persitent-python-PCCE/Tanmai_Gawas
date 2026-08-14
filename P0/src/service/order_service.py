from src.utils.logger import log_action
from src.models.product import Product
from src.utils.query import QuerySpec, PageResult
from src.dao.order_dao import ALLOWED_ORDER_SORT_FIELDS
from src.utils.send_email import send_order_placed_email

class OrderService:
    def __init__(self, order_dao, product_dao, cart_service):
        self.order_dao = order_dao
        self.product_dao = product_dao
        self.cart_service = cart_service

    def place_order(self, user_id, email, full_name):
        summary = self.cart_service.get_cart_summary(user_id)
        if not summary:
            raise ValueError("Cart is empty. Add products before placing an order.")

        items_to_checkout = []
        for item in summary:
            p = item["product"]
            qty = item["quantity"]
            
            fresh_p = self.product_dao.get_by_id(p.product_id)
            if not fresh_p or fresh_p.stock < qty:
                raise ValueError(
                    f"Checkout failed: Insufficient stock for '{p.name}'. "
                    f"Available: {fresh_p.stock if fresh_p else 0}"
                )
            items_to_checkout.append({
                "product_id": p.product_id,
                "product_name": p.name,
                "quantity": qty,
                "price": float(p.price)
            })

        total_price = self.cart_service.get_cart_total(user_id)
        try:
            order_id = self.order_dao.place_order_transaction(user_id, total_price, items_to_checkout)
            log_action(f"Order #{order_id} placed successfully by '{full_name}'. Total: ${total_price:.2f}")
            self.cart_service.clear_cart(user_id)
            send_order_placed_email(email, full_name, order_id, total_price, items_to_checkout)
            return order_id
        except Exception as e:
            log_action(f"Order placement failed for '{full_name}': {e}", "error")
            raise e

    def get_order_history(self, user_id):
        orders = self.order_dao.get_orders_by_user_id(user_id)
        history = []
        for o in orders:
            items = self.order_dao.get_order_items_by_order_id(o["id"])
            history.append({
                "order_id": o["id"],
                "order_date": o["order_date"],
                "total_price": float(o["total_price"]),
                "items": items
            })
        return history

    def get_all_orders(self):
        orders = self.order_dao.get_all_orders()
        all_orders = []
        for o in orders:
            items = self.order_dao.get_order_items_by_order_id(o["id"])
            all_orders.append({
                "order_id": o["id"],
                "full_name": o["full_name"],
                "order_date": o["order_date"],
                "total_price": float(o["total_price"]),
                "items": items
            })
        return all_orders

    def browse_orders(self, filters=None, search=None, sort_by=None, sort_dir="ASC", page=1, page_size=10):
        if sort_by and sort_by not in ALLOWED_ORDER_SORT_FIELDS:
            raise ValueError(f"Cannot sort by '{sort_by}'. Allowed: {', '.join(ALLOWED_ORDER_SORT_FIELDS)}")

        spec = QuerySpec(filters, search, sort_by, sort_dir, page, page_size)
        rows, total = self.order_dao.search_orders(spec)

        orders = []
        for o in rows:
            items = self.order_dao.get_order_items_by_order_id(o["id"])
            orders.append({
                "order_id": o["id"],
                "full_name": o["full_name"],
                "order_date": o["order_date"],
                "total_price": float(o["total_price"]),
                "items": items
            })
        return PageResult(orders, total, spec.page, spec.page_size)
