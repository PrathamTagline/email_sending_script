import csv
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from pathlib import Path

# ===== LOAD ENVIRONMENT VARIABLES =====
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# ===== GLOBAL CONFIGURATION FROM .env =====
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_EMAIL_PASSWORD = os.getenv("SENDER_EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
USE_SSL = os.getenv("SMTP_USE_SSL", "False").strip().lower() == "true"
CONTACTS_FILE = os.getenv("CONTACTS_FILE_PATH")

# ===== EMAIL SUBJECT AND BODY TEMPLATE =====
SUBJECT = "Business Collaboration Opportunity"
BODY_TEMPLATE = """
Hi {ownername},

I hope this message finds you well. I came across your business, {businessname}, and I believe there could be a great opportunity for collaboration.

Let's connect soon!

Best regards,  
Your Name
"""

# ===== FUNCTION TO SEND EMAIL =====
def send_email(to_email, ownername, businessname):
    """
    Sends an email to the specified recipient with the provided owner and business names.
    Args:
        to_email (str): The recipient's email address.
        ownername (str): The name of the business owner.
        businessname (str): The name of the business.
    """
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = to_email
    message["Subject"] = SUBJECT

    body = BODY_TEMPLATE.format(ownername=ownername, businessname=businessname)
    message.attach(MIMEText(body, "plain"))

    if USE_SSL:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
            server.send_message(message)
    else:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_EMAIL_PASSWORD)
            server.send_message(message)

# ===== FUNCTION TO PROCESS CONTACTS =====
def process_contacts(csv_file):
    """
    Reads a CSV file containing contact information and sends emails to each contact.
    Args:
        csv_file (str): Path to the CSV file containing contact information.
    """
    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            send_email(
                to_email=row["email"],
                ownername=row["ownername"],
                businessname=row["businessname"]
            )

# ===== MAIN ENTRY POINT =====
def main():
    """
    Main function to execute the email sending process.
    Checks for required environment variables and processes the contacts file.
    """
    if not all([SENDER_EMAIL, SENDER_EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT, CONTACTS_FILE]):
        return 
    process_contacts(CONTACTS_FILE)

if __name__ == "__main__":
    main()
