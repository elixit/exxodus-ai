import smtplib
import json
import os
from email.mime.text import MIMEText
from twilio.rest import Client
from dotenv import load_dotenv

# ✅ Load Environment Variables from .env
load_dotenv()

# ✅ Load Config from .env
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

LEADS_FILE = "backend/leads.json"  # ✅ Ensure the correct path

# ✅ Load leads from `leads.json`
def load_leads():
    if not os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "w") as file:
            json.dump([], file)  # ✅ Initialize empty list if missing
    try:
        with open(LEADS_FILE, "r") as file:
            return json.load(file)  # ✅ Returns a LIST of leads
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # ✅ Returns empty list instead of crashing

leads = load_leads()  # ✅ Now contains a list

# ✅ Send an email to a lead
def send_email(to_email, subject, body):
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = SMTP_USERNAME
        msg["To"] = to_email

        server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent successfully to {to_email}")
    except Exception as e:
        print(f"❌ Email failed: {e}")

# ✅ Send an SMS to a lead
def send_sms(to_number, message):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(body=message, from_=TWILIO_PHONE_NUMBER, to=to_number)
        print(f"✅ SMS sent successfully to {to_number}")
    except Exception as e:
        print(f"❌ SMS failed: {e}")

# ✅ Send outreach to each lead in `leads.json`
for lead in leads:
    email_body = f"Hello {lead['name']},\n\nWe offer AI-powered lead generation solutions to help you grow your business. Let’s connect!"
    
    send_email(lead["name"], "AI Lead Generation Offer", email_body)
    send_sms("+1234567890", f"Hey {lead['name']}, AI can get you more customers!")
