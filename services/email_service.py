import os
import smtplib
from email.mime.text import MIMEText


def send_email(html_content: str):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    recipient = os.getenv("EMAIL_TO")

    msg = MIMEText(html_content, "html")

    msg["Subject"] = "Daily Tech News Summary"
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
