import os
import smtplib
from email.message import EmailMessage
import hashlib
import random
from dotenv import load_dotenv


load_dotenv()
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

        otp_hash = hashlib.sha256(
            otp.encode("utf-8")
        ).hexdigest()

        return otp_hash

    except Exception as e:
        print("Failed to send email:", e)
        return None

send_otp_email('gawastanmay373@gmail.com')