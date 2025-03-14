from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER
import json
import time

# Load client data
def load_clients():
    with open("backend/clients.json", "r") as file:
        return json.load(file)

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Function to make a call and play a message
def make_call(to_number, message):
    call = twilio_client.calls.create(
        twiml=f'<Response><Say>{message}</Say></Response>',
        to=to_number,
        from_=TWILIO_PHONE_NUMBER
    )
    print(f"Calling {to_number} - Call SID: {call.sid}")

# Function to call all leads for a client
def call_leads():
    clients = load_clients()

    for client_email, client_data in clients.items():
        leads = client_data.get("leads", [])

        for lead in leads:
            phone_number = lead.get("phone")  # Ensure phone numbers are stored in `clients.json`
            if phone_number:
                message = f"Hello, this is an automated call from our AI lead generation system. We can help your business generate more customers using AI automation. Press 1 to learn more."
                make_call(phone_number, message)
                time.sleep(2)  # Prevent spam calling

# Run the callbot
if __name__ == "__main__":
    call_leads()
