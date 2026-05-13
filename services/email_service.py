import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


def send_email(date: str, html_content: str, image_paths: list = None):
    """
    Send HTML email with optional images.
    
    Args:
        html_content: HTML content for the email body
        image_paths: Optional list of image file paths to attach
    """
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    recipient = os.getenv("EMAIL_TO")

    # Use MIMEMultipart for emails with attachments
    if image_paths:
        msg = MIMEMultipart("related")
        msg_alternative = MIMEMultipart("alternative")
        msg.attach(msg_alternative)
        msg_alternative.attach(MIMEText(html_content, "html"))

        # Attach images
        for image_path in image_paths:
            if os.path.exists(image_path):
                with open(image_path, "rb") as attachment:
                    image = MIMEImage(attachment.read())
                    image.add_header("Content-ID",
                                     f"<{os.path.basename(image_path)}>")
                    msg.attach(image)
    else:
        # Simple HTML email without images
        msg = MIMEText(html_content, "html")

    msg["Subject"] = f"the paper boy: {date} delivery"
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)
