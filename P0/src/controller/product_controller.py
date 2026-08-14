from src.utils.inputs import get_int_input, get_float_input

class ProductController:
    def __init__(self, product_service):
        self.product_service = product_service

    def display_catalog(self):
        """Retrieve and display products catalog."""
        products = self.product_service.get_all_products()
        print("\n" + "=" * 80)
        print(f"{'PRODUCT CATALOG':^80}")
        print("=" * 80)
        if not products:
            print(f"{'No products available in the catalog.':^80}")
        else:
            print(f"{'ID':<6} | {'Name':<20} | {'Price':<12} | {'Stock':<8} | {'Description'}")
            print("-" * 80)
            for p in products:
                print(f"{p.product_id:<6} | {p.name:<20} | ${p.price:<11.2f} | {p.stock:<8} | {p.description or ''}")
        print("=" * 80 + "\n")

    def add_product_menu(self, admin):
        print("\n--- ADD NEW PRODUCT ---")
        name = input("Enter product name: ").strip()
        if not name:
            print("  [!] Name cannot be empty.")
            return
        desc = input("Enter description: ").strip()
        price = get_float_input("Enter price: ", min_val=0.01)
        stock = get_int_input("Enter initial stock quantity: ", min_val=0)
        try:
            pid = self.product_service.add_product(name, desc, price, stock, admin.full_name)
            print(f"  [OK] Product '{name}' added successfully with ID {pid}.")
        except ValueError as e:
            print(f"  [!] Error: {e}")

    def update_product_menu(self, admin):
        print("\nRun a search first (option 7), then select a product to update (option 8).")
        prod = self.browse_menu(select_mode=True)
        if not prod:
            return

        print(f"\nUpdating product ID {prod.product_id} ('{prod.name}')")
        print("Leave input blank to keep current value.")

        name = input(f"New name [{prod.name}]: ").strip() or None
        desc = input(f"New description [{prod.description or ''}]: ").strip()
        desc = desc if desc else None

        price = get_float_input(f"New price [${prod.price:.2f}]: ", min_val=0.01, allow_blank=True)
        stock = get_int_input(f"New stock quantity [{prod.stock}]: ", min_val=0, allow_blank=True)

        try:
            self.product_service.update_product(prod.product_id, name, desc, price, stock, admin.full_name)
            print("  [OK] Product updated successfully.")
        except ValueError as e:
            print(f"  [!] Error: {e}")

    def delete_product_menu(self, admin):
        print("\nRun a search first (option 7), then select a product to delete (option 8).")
        prod = self.browse_menu(select_mode=True)
        if not prod:
            return

        confirm = input(f"Are you sure you want to delete product ID {prod.product_id} ('{prod.name}')? (y/n): ").strip().lower()
        if confirm == 'y':
            try:
                self.product_service.delete_product(prod.product_id, admin.full_name)
                print("  [OK] Product deleted successfully.")
            except ValueError as e:
                print(f"  [!] Error: {e}")
        else:
            print("  [!] Deletion canceled.")

    def bulk_upload_menu(self, admin):
        print("\n--- BULK UPLOAD PRODUCTS ---")
        file_path = input("Enter path to CSV file: ").strip()
        if not file_path:
            print("  [!] File path cannot be empty.")
            return
        try:
            result = self.product_service.bulk_upload(file_path, admin.full_name)
            print(f"  [OK] Bulk upload completed successfully!")
            print(f"  Products Inserted: {result['inserted']}")
            if result['failed']:
                print(f"  Failed rows:")
                for row_idx, err in result['failed']:
                    print(f"    - Row {row_idx}: {err}")
        except ValueError as e:
            print(f"  [!] Error: {e}")
        except Exception as e:
            print(f"  [!] System error during bulk upload: {e}")

    def browse_menu(self, select_mode=False):
        filters = {}
        search = None
        sort_by = None
        sort_dir = "ASC"
        page = 1
        last_result = None

        while True:
            print("\n--- BROWSE PRODUCTS ---")
            print(f"  Current filters : {filters or 'none'}")
            print(f"  Current search  : {search or 'none'}")
            print(f"  Current sort    : {sort_by or 'none'} {sort_dir if sort_by else ''}")
            print(f"  Current page    : {page}")
            print("-" * 40)
            print("  1. Set price range")
            print("  2. Toggle in-stock only")
            print("  3. Set search term")
            print("  4. Set sort field/direction")
            print("  5. Set page number")
            print("  6. Clear all filters")
            print("  7. Run search")
            if select_mode and last_result and last_result.items:
                print("  8. Select a product from results")
            print("  9. Back")

            max_choice = 9
            choice = get_int_input("Select an option: ", min_val=1, max_val=max_choice)

            if choice == 1:
                price_min = get_float_input("Min price (blank to skip): ", min_val=0, allow_blank=True)
                price_max = get_float_input("Max price (blank to skip): ", min_val=0, allow_blank=True)
                if price_min is not None:
                    filters["price_min"] = price_min
                else:
                    filters.pop("price_min", None)
                if price_max is not None:
                    filters["price_max"] = price_max
                else:
                    filters.pop("price_max", None)

            elif choice == 2:
                filters["in_stock"] = not filters.get("in_stock", False)
                print(f"  In-stock only: {filters['in_stock']}")

            elif choice == 3:
                term = input("Search term (blank to clear): ").strip()
                search = term or None

            elif choice == 4:
                field = input("Sort by (name/price/stock/created_at, blank to clear): ").strip()
                sort_by = field or None
                if sort_by:
                    sort_dir = input("Direction (ASC/DESC) [ASC]: ").strip().upper() or "ASC"

            elif choice == 5:
                page = get_int_input("Page number: ", min_val=1)

            elif choice == 6:
                filters, search, sort_by, sort_dir, page = {}, None, None, "ASC", 1
                print("  [OK] Cleared.")

            elif choice == 7:
                try:
                    last_result = self.product_service.browse(filters, search, sort_by, sort_dir, page, 10)
                except ValueError as e:
                    print(f"  [!] Error: {e}")
                    continue

                print("\n" + "=" * 80)
                print(f"{'ID':<6} | {'Name':<20} | {'Price':<12} | {'Stock':<8} | {'Description'}")
                print("-" * 80)
                if not last_result.items:
                    print(f"{'No matching products.':^80}")
                for p in last_result.items:
                    print(f"{p.product_id:<6} | {p.name:<20} | ${p.price:<11.2f} | {p.stock:<8} | {p.description or ''}")
                print("-" * 80)
                print(f"Page {last_result.page}/{last_result.total_pages} ({last_result.total} total results)")
                print("=" * 80 + "\n")

                new_page = get_int_input(
                    f"Jump to page (1-{last_result.total_pages}) [{page}]: ",
                    min_val=1, max_val=last_result.total_pages, allow_blank=True
                )
                if new_page:
                    page = new_page

            elif choice == 8 and select_mode and last_result and last_result.items:
                pid = get_int_input("Enter Product ID to select: ", min_val=1)
                selected = next((p for p in last_result.items if p.product_id == pid), None)
                if not selected:
                    print("  [!] That ID isn't in the current results.")
                    continue
                return selected

            elif choice == 9:
                return None