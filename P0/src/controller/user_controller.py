from src.utils.inputs import get_int_input

class CustomerController:
    def __init__(self, product_controller, cart_controller, order_controller, customer_service):
        self.product_controller = product_controller
        self.cart_controller = cart_controller
        self.order_controller = order_controller
        self.customer_service = customer_service

    def customer_dashboard(self, customer):
        while True:
            print("\n" + "*" * 50)
            print(f" CUSTOMER DASHBOARD - Welcome, {customer.full_name if customer.full_name is not None else customer.email}!")
            print("*" * 50)
            menu = customer.get_dashboard_menu()
            for idx, option in enumerate(menu, 1):
                print(f"  {idx}. {option}")
            print("*" * 50)
            
            choice = get_int_input("Select an option: ", min_val=1, max_val=len(menu))
            selected_option = menu[choice - 1]

            if selected_option == "View All Products":
                self.product_controller.display_catalog()

            elif selected_option == "Search / Filter Products":
                self.product_controller.browse_menu()

            elif selected_option == "Add to Cart":
                self.cart_controller.add_to_cart_menu(customer)

            elif selected_option == "Remove from Cart":
                self.cart_controller.remove_from_cart_menu(customer)

            elif selected_option == "View Cart Summary":
                self.cart_controller.view_cart_summary(customer)

            elif selected_option == "Place Order":
                self.order_controller.place_order_menu(customer)

            elif selected_option == "View Order History":
                self.order_controller.view_order_history_menu(customer)

            elif selected_option == "Update Profile":
                self.view_update_menu(customer)

            elif selected_option == "Logout":
                print(f"Logging out {customer.full_name if customer.full_name is not None else customer.email}...")
                break

    def admin_dashboard(self, admin):
        while True:
            print("\n" + "#" * 50)
            print(f" ADMIN DASHBOARD - Welcome, {admin.full_name if admin.full_name is not None else admin.email} [ADMIN]")
            print("#" * 50)
            menu = admin.get_dashboard_menu()
            for idx, option in enumerate(menu, 1):
                print(f"  {idx}. {option}")
            print("#" * 50)
            
            choice = get_int_input("Select an option: ", min_val=1, max_val=len(menu))
            selected_option = menu[choice - 1]

            if selected_option == "View All Products":
                self.product_controller.display_catalog()

            elif selected_option == "Search / Filter Products":
                self.product_controller.browse_menu()

            elif selected_option == "Add Product":
                self.product_controller.add_product_menu(admin)

            elif selected_option == "Update Product":
                self.product_controller.update_product_menu(admin)

            elif selected_option == "Delete Product":
                self.product_controller.delete_product_menu(admin)

            elif selected_option == "Bulk Upload Products":
                self.product_controller.bulk_upload_menu(admin)

            elif selected_option == "View All Orders":
                self.order_controller.view_all_orders_menu(admin)

            elif selected_option == "Search / Filter Orders":
                self.order_controller.browse_orders_menu(admin)

            elif selected_option == "Export Database (Backup)":
                self.export_database_menu(admin)

            elif selected_option == "Logout":
                print(f"Logging out {admin.full_name if admin.full_name is not None else admin.email}...")
                break

    def export_database_menu(self, admin):
        print("\n--- DATABASE EXPORT / BACKUP ---")
        print("  1. Export to CSV")
        print("  2. Export to JSON")
        fmt_choice = get_int_input("Select format (1 or 2): ", min_val=1, max_val=2)
        fmt = "csv" if fmt_choice == 1 else "json"
        
        try:
            print("Exporting tables: users, products, orders, order_items...")
            paths = self.customer_service.run_backup(fmt)
            print("  [OK] Export completed successfully!")
            print("  Files saved:")
            for p in paths:
                print(f" - {p}")
        except Exception as e:
            print(f"  [!] Backup failed: {e}")

    def view_update_menu(self, customer):
            while True:
                print("\n--- UPDATE PROFILE ---")
                print("1. Update Phone")
                print("2. Update Address")
                print("3. Update Date of Birth")
                print("4. Update All")
                print("5. Back")
    
                choice = get_int_input("Select an option: ", min_val=1, max_val=5)
    
                if choice == 1:
                    phone = input("Enter new phone: ").strip()
                    try:
                        print(customer.address)
                        self.customer_service.update_user(
                            customer.user_id,
                            phone,
                            customer.address,
                            customer.date_of_birth
                        )
                        customer.phone = phone
                        print("  [OK] Phone updated successfully.")

                    except Exception as e:
                        print(f"  [!] Update failed: {e}")
    
                elif choice == 2:
                    address = input("Enter new address: ").strip()
    
                    try:
                        self.customer_service.update_user(
                            customer.user_id,
                            customer.phone,
                            address,
                            customer.date_of_birth
                        )
                        customer.address = address
                        print("  [OK] Address updated successfully.")
    
                    except Exception as e:
                        print(f"  [!] Update failed: {e}")
    
                elif choice == 3:
                    date_of_birth = input(
                        "Enter date of birth YYYY-MM-DD: "
                    ).strip()
    
                    try:
                        self.customer_service.update_user(
                            customer.user_id,
                            customer.phone,
                            customer.address,
                            date_of_birth
                        )
                        customer.date_of_birth = date_of_birth
                        print("  [OK] Date of birth updated successfully.")
    
                    except Exception as e:
                        print(f"  [!] Update failed: {e}")
    
                elif choice == 4:
                    phone = input("Enter new phone: ").strip()
                    address = input("Enter new address: ").strip()
                    date_of_birth = input(
                        "Enter date of birth YYYY-MM-DD: "
                    ).strip()
    
                    try:
                        self.customer_service.update_user(
                            customer.user_id,
                            phone,
                            address,
                            date_of_birth
                        )
                        customer.phone = phone
                        customer.address = address
                        customer.date_of_birth = date_of_birth
                        print("  [OK] Profile updated successfully.")
    
                    except Exception as e:
                        print(f"  [!] Update failed: {e}")
    
                elif choice == 5:
                    break
