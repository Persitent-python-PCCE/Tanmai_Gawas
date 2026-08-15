import os
import smtplib
from email.message import EmailMessage
import hashlib
import random

sender_email = os.environ.get("EMAIL")
app_password = os.environ.get("APP_PASSWORD")


def send_otp_email(email):
    try:
        receiver_email = email.strip()

        otp = str(random.randint(100000, 999999))

        msg = EmailMessage()
        msg["Subject"] = "Your E-Commerce OTP"
        msg["From"] = sender_email
        msg["To"] = receiver_email

        msg.set_content(
            f"Your OTP for E-Commerce Registration is: {otp}"
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)

        print("OTP sent successfully!")

        # Hash OTP before returning it
        otp_hash = hashlib.sha256(
            otp.encode("utf-8")
        ).hexdigest()

        return otp_hash

    except Exception as e:
        print("Failed to send email:", e)
        return None

def send_order_placed_email(email, full_name, order_id, total_price, items):
    try:
        receiver_email = email.strip()

        msg = EmailMessage()
        msg["Subject"] = "Your E-Commerce Order Confirmation"
        msg["From"] = sender_email
        msg["To"] = receiver_email

        msg.set_content(
            f"Hello {full_name},\n\nYour order has been placed successfully!\n\nOrder ID: {order_id}\nTotal Price: ${total_price:.2f}\n\nItems:"
        )

        for item in items:
            msg.set_content(
                f"{msg.get_content()}\n- {item['product_name']} x{item['quantity']} @ ${float(item['price']):.2f}"
            )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            smtp.send_message(msg)

        print("Order confirmation email sent successfully!")
        return True

    except Exception as e:
        print("Failed to send email:", e)
        return False

