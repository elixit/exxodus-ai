from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Stripe API
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")

# Twilio API
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# OpenAI API
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Apollo API
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY")

# Email SMTP
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = os.getenv("SMTP_PORT")
