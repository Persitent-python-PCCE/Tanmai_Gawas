from src.utils.inputs import get_int_input, get_float_input

class OrderController:
    def __init__(self, order_service):
        self.order_service = order_service

    def place_order_menu(self, customer):
        summary = self.order_service.cart_service.get_cart_summary(customer.user_id)
        if not summary:
            print("  [!] Cart is empty. Add products before placing an order.")
            return

        print("\n--- CHECKOUT ---")
        print("  1. Checkout all items")
        print("  2. Select specific items to checkout")
        print("  3. Cancel")
        
        choice = get_int_input("Select checkout option: ", min_val=1, max_val=3)
        if choice == 3:
            return

        product_ids = None
        if choice == 2:
            print("\nItems in your cart:")
            for idx, item in enumerate(summary, 1):
                p = item["product"]
                qty = item["quantity"]
                print(f"  {idx}. {p.name} x{qty} @ ${float(p.price):.2f} (Subtotal: ${item['subtotal']:.2f})")
            
            indices_input = input("\nEnter the numbers of the items to checkout (comma-separated, e.g. 1,3): ").strip()
            if not indices_input:
                print("  [!] No items selected. Checkout cancelled.")
                return
            
            try:
                indices = [int(x.strip()) - 1 for x in indices_input.split(",") if x.strip()]
                selected_items = [summary[idx] for idx in indices if 0 <= idx < len(summary)]
                if not selected_items:
                    print("  [!] No valid items selected. Checkout cancelled.")
                    return
                product_ids = [item["product"].product_id for item in selected_items]
            except Exception:
                print("  [!] Invalid input format. Checkout cancelled.")
                return

        try:
            order_id = self.order_service.place_order(
                customer.user_id,
                customer.email,
                customer.full_name,
                product_ids=product_ids
            )
            print(f"\n  [OK] Order #{order_id} placed successfully! Thank you for shopping with us.")
        except ValueError as e:
            print(f"  [!] Order failed: {e}")

    def view_order_history_menu(self, customer):
        history = self.order_service.get_order_history(customer.user_id)
        print("\n" + "=" * 75)
        print(f"{'YOUR ORDER HISTORY':^75}")
        print("=" * 75)
        if not history:
            print(f"{'You have not placed any orders yet.':^75}")
        else:
            for o in history:
                print(f"Order #{o['order_id']} | Date: {o['order_date']} | Status: {o['status']} | Total: ${o['total_price']:.2f}")
                print("  Items:")
                for item in o["items"]:
                    print(f"    - {item['product_name']} x{item['quantity']} @ ${float(item['price']):.2f}")
                print("-" * 75)
        print("=" * 75 + "\n")

    def view_all_orders_menu(self, admin):
        all_orders = self.order_service.get_all_orders()
        print("\n" + "=" * 90)
        print(f"{'SYSTEM ORDERS REPORT':^90}")
        print("=" * 90)
        if not all_orders:
            print(f"{'No orders placed in the system yet.':^90}")
        else:
            for o in all_orders:
                print(f"Order #{o['order_id']} | User: {o['full_name']} | Date: {o['order_date']} | Status: {o['status']} | Total: ${o['total_price']:.2f}")
                print("  Items:")
                for item in o["items"]:
                    print(f"    - {item['product_name']} (ID: {item['product_id']}) x{item['quantity']} @ ${float(item['price']):.2f}")
                print("-" * 90)
        print("=" * 90 + "\n")


    def browse_orders_menu(self, admin):
        filters = {}
        search = None
        sort_by = None
        sort_dir = "DESC"
        page = 1
        last_result = None

        while True:
            print("\n--- BROWSE ORDERS ---")
            print(f"  Current filters : {filters or 'none'}")
            print(f"  Current search  : {search or 'none'} (customer name)")
            print(f"  Current sort    : {sort_by or 'order_date'} {sort_dir}")
            print(f"  Current page    : {page}")
            print("-" * 40)
            print("  1. Set order date range")
            print("  2. Set total price range")
            print("  3. Set search term (customer name)")
            print("  4. Set sort field/direction")
            print("  5. Set page number")
            print("  6. Clear all filters")
            print("  7. Run search")
            print("  8. Back")

            choice = get_int_input("Select an option: ", min_val=1, max_val=8)

            if choice == 1:
                date_from = input("From date (YYYY-MM-DD, blank to skip): ").strip()
                date_to = input("To date (YYYY-MM-DD, blank to skip): ").strip()
                if date_from:
                    filters["date_from"] = date_from
                else:
                    filters.pop("date_from", None)
                if date_to:
                    filters["date_to"] = date_to
                else:
                    filters.pop("date_to", None)

            elif choice == 2:
                total_min = get_float_input("Min total (blank to skip): ", min_val=0, allow_blank=True)
                total_max = get_float_input("Max total (blank to skip): ", min_val=0, allow_blank=True)
                if total_min is not None:
                    filters["total_min"] = total_min
                else:
                    filters.pop("total_min", None)
                if total_max is not None:
                    filters["total_max"] = total_max
                else:
                    filters.pop("total_max", None)

            elif choice == 3:
                term = input("Customer name search (blank to clear): ").strip()
                search = term or None

            elif choice == 4:
                field = input("Sort by (order_date/total_price, blank for default): ").strip()
                sort_by = field or None
                if sort_by:
                    sort_dir = input("Direction (ASC/DESC) [DESC]: ").strip().upper() or "DESC"

            elif choice == 5:
                page = get_int_input("Page number: ", min_val=1)

            elif choice == 6:
                filters, search, sort_by, sort_dir, page = {}, None, None, "DESC", 1
                print("  [OK] Cleared.")

            elif choice == 7:
                try:
                    last_result = self.order_service.browse_orders(filters, search, sort_by, sort_dir, page, 10)
                except ValueError as e:
                    print(f"  [!] Error: {e}")
                    continue

                print("\n" + "=" * 80)
                print(f"{'SYSTEM ORDERS REPORT':^80}")
                print("=" * 80)
                if not last_result.items:
                    print(f"{'No matching orders.':^80}")
                for o in last_result.items:
                    print(f"Order #{o['order_id']} | User: {o['full_name']} | Date: {o['order_date']} | Status: {o['status']} | Total: ${o['total_price']:.2f}")
                    print("  Items:")
                    for item in o["items"]:
                        print(f"    - {item['product_name']} (ID: {item['product_id']}) x{item['quantity']} @ ${float(item['price']):.2f}")
                    print("-" * 80)
                print(f"Page {last_result.page}/{last_result.total_pages} ({last_result.total} total orders)")
                print("=" * 80 + "\n")

                new_page = get_int_input(
                    f"Jump to page (1-{last_result.total_pages}) [{page}]: ",
                    min_val=1, max_val=last_result.total_pages, allow_blank=True
                )
                if new_page:
                    page = new_page

            elif choice == 8:
                return

    def approve_order_menu(self, admin):
        print("\n--- APPROVE ORDER ---")
        order_id = get_int_input("Enter Order ID to approve: ", min_val=1)
        try:
            self.order_service.approve_order(order_id)
            print(f"  [OK] Order #{order_id} has been successfully approved.")
        except ValueError as e:
            print(f"  [!] Operation failed: {e}")
