import os
import sys

# Ensure the root folder is on the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.database import get_connection
from dao.user_dao import CustomerDAO
from dao.product_dao import ProductDAO
from dao.cart_dao import CartDAO
from dao.order_dao import OrderDAO

from src.service.auth_service import AuthService
from src.service.product_service import ProductService
from src.service.cart_service import CartService
from src.service.order_service import OrderService
from service.user_service import CustomerService

from src.controller.product_controller import ProductController
from src.controller.cart_controller import CartController
from src.controller.order_controller import OrderController
from controller.user_controller import CustomerController
from src.controller.auth_controller import AuthController

from src.utils.inputs import get_int_input

def main():
    print("\n" + "=" * 50)
    print(f"{'CONSOLE E-COMMERCE SYSTEM':^50}")
    print("=" * 50)
    print("Initializing system environment...")
    
    try:
        conn = get_connection()
        conn.close()

        # schema_path = os.path.abspath(
        # os.path.join(os.path.dirname(__file__), "..", "schema.sql")
        # )

        # execute_sql_file(schema_path)

        print("  [OK] Database environment initialized.")
    except Exception as e:
        print(f"\n  [!] CRITICAL ERROR: Could not connect to MySQL database.")
        print(f"  Details: {e}")
        print("\n  Please verify:")
        print("  1. MySQL server is running locally on port 3306 (or configured DB_PORT).")
        print("  2. DB user/password matches defaults or DB_USER/DB_PASSWORD env variables.")
        print("  3. MySQL client/connector is accessible.")
        print("\nExiting application...")
        sys.exit(1)

    # Initialize daository / DAO Layer
    customer_dao = CustomerDAO()
    product_dao = ProductDAO()
    cart_dao = CartDAO(product_dao)
    order_dao = OrderDAO()

    # Initialize Service Layer
    auth_service = AuthService(customer_dao)
    product_service = ProductService(product_dao)
    cart_service = CartService(cart_dao, product_dao)
    order_service = OrderService(order_dao, product_dao, cart_service)
    customer_service = CustomerService(customer_dao)

    # Initialize Controller Layer
    product_controller = ProductController(product_service)
    cart_controller = CartController(cart_service, product_service, product_controller)
    order_controller = OrderController(order_service)
    customer_controller = CustomerController(
        product_controller, cart_controller, order_controller, customer_service
    )
    auth_controller = AuthController(auth_service, customer_controller)

    while True:
        print("\n" + "=" * 50)
        print(f"{'MAIN MENU':^50}")
        print("=" * 50)
        print("  1. Register New Account")
        print("  2. Login Existing Account")
        print("  3. Exit")
        print("=" * 50)
        
        choice = get_int_input("Select an option: ", min_val=1, max_val=3)

        if choice == 1:
            auth_controller.register_menu()
        elif choice == 2:
            auth_controller.login_menu()
        elif choice == 3:
            print("\nThank you for using Console E-Commerce. Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
        sys.exit(0)
