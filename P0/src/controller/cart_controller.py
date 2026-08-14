from src.utils.inputs import get_int_input

class CartController:
    def __init__(self, cart_service, product_service, product_controller):
        self.cart_service = cart_service
        self.product_service = product_service
        self.product_controller = product_controller

    def add_to_cart_menu(self, customer):
        print("\nRun a search first (option 7), then select a product to add (option 8).")
        prod = self.product_controller.browse_menu(select_mode=True)
        if not prod:
            return  # user backed out without selecting anything

        qty = get_int_input(f"Enter quantity (Available: {prod.stock}): ", min_val=1)
        try:
            self.cart_service.add_to_cart(customer.user_id, prod, qty)
            print(f"  [OK] Added {qty}x '{prod.name}' to cart.")
        except ValueError as e:
            print(f"  [!] Error: {e}")

    def remove_from_cart_menu(self, customer):
        summary = self.cart_service.get_cart_summary(customer.user_id)
        if not summary:
            print("  [!] Your shopping cart is empty.")
            return
        
        print("\n--- YOUR CART ---")
        for item in summary:
            p = item["product"]
            print(f"  ID: {p.product_id} | {p.name:<20} | Quantity: {item['quantity']}")
        
        pid = get_int_input("Enter Product ID to remove: ", min_val=1)
        cart_item = next((item for item in summary if item["product"].product_id == pid), None)
        if not cart_item:
            print("  [!] That product is not in your cart.")
            return
        
        max_qty = cart_item["quantity"]
        qty = get_int_input(f"Enter quantity to remove (max {max_qty}, enter empty to remove all): ", min_val=1, allow_blank=True)
        try:
            self.cart_service.remove_from_cart(customer.user_id, pid, qty)
            if qty is None:
                print("  [OK] Removed item completely from cart.")
            else:
                print(f"  [OK] Removed {qty} units of item from cart.")
        except ValueError as e:
            print(f"  [!] Error: {e}")

    def view_cart_summary(self, customer):
        summary = self.cart_service.get_cart_summary(customer.user_id)
        print("\n" + "=" * 60)
        print(f"{'SHOPPING CART SUMMARY':^60}")
        print("=" * 60)
        if not summary:
            print(f"{'Your cart is empty.':^60}")
        else:
            print(f"{'Product':<25} | {'Price':<10} | {'Qty':<5} | {'Subtotal'}")
            print("-" * 60)
            for item in summary:
                p = item["product"]
                print(f"{p.name:<25} | ${p.price:<9.2f} | {item['quantity']:<5} | ${item['subtotal']:.2f}")
            print("-" * 60)
            total = self.cart_service.get_cart_total(customer.user_id)
            print(f"{'TOTAL:':<44} | ${total:.2f}")
        print("=" * 60 + "\n")
