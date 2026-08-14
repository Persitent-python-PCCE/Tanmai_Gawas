from src.utils.inputs import get_int_input
from src.models.admin import Admin
from src.models.customer import Customer
from src.utils.logger import log_action
from src.utils.send_email import send_otp_email

class AuthController:
    def __init__(self, auth_service, customer_controller):
        self.auth_service = auth_service
        self.customer_controller = customer_controller

    def register_menu(self):
        print("\n--- REGISTER ACCOUNT ---")

        email = input("Enter email: ").strip()
        password = input("Enter password: ")
        full_name = input("Enter Full Name(optional): ").strip() or None
        phone = input("Enter phone(optional): ").strip() or None
        address = input("Enter address(optional): ").strip() or None
        date_of_birth = input(
            "Enter date of birth YYYY-MM-DD(optional): "
        ).strip() or None

        role = "customer"

        try:
            if not self.auth_service.verify_email(email):
                raise ValueError("Invalid email format.")

            otp_hash = send_otp_email(email)

            if not otp_hash:
                raise ValueError("Could not send OTP.")

            user_otp = input(
                "Enter the OTP sent to your email: "
            ).strip()

            verified = self.auth_service.verify_otp(
                user_otp,
                otp_hash
            )

            if not verified:
                raise ValueError("OTP verification failed.")

            self.auth_service.register_user(
                full_name=full_name,
                password=password,
                email=email,
                phone=phone,
                address=address,
                date_of_birth=date_of_birth,
                role=role,
            )

            print(
                f"  [OK] Account created successfully "
                f"for '{full_name}' as '{role}'."
            )

        except ValueError as e:
            print(f"  [!] Registration failed: {e}")

        except Exception as e:
            print(
                f"  [!] System error during registration: {e}"
            )

    def login_menu(self):
        print("\n--- USER LOGIN ---")
        email = input("Email: ").strip()
        password = input("Password: ")
        
        user_data = self.auth_service.login_user(email, password)
        if user_data:
            if user_data["role"] == "admin":
                user_instance = user_instance = Admin(
                                user_data["id"],
                                user_data["full_name"],
                                user_data["email"],
                                user_data["phone"],
                                user_data["address"],
                                user_data["date_of_birth"])
                self.customer_controller.admin_dashboard(user_instance)
            else:
                user_instance = Customer(
                user_data["id"],
                user_data["full_name"],
                user_data["email"],
                user_data["phone"],
                user_data["address"],
                user_data["date_of_birth"]
            )
                self.customer_controller.customer_dashboard(user_instance)
        else:
            print("  [!] Invalid email or password.")
