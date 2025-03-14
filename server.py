from flask import Flask, render_template, request, jsonify
import json
import stripe
import os
import requests
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
stripe.api_key = STRIPE_SECRET_KEY

app = Flask(__name__, template_folder="frontend/templates")

# ✅ Store users for login (Temporary; use a database later)
users = {
    "test@example.com": "password123"  # ✅ Test user
}

# ✅ Home Route (Landing Page)
@app.route("/")
def home():
    return render_template("index.html")

# ✅ Payment Page (Renders Payment Form)
@app.route("/payment")
def payment():
    return render_template("payment.html")

# ✅ Payment Success Page
@app.route("/payment-success")
def payment_success():
    return render_template("success.html")

# ✅ Payment Failed Page
@app.route("/payment-failed")
def payment_failed():
    return "❌ Payment Failed. Please try again."

# ✅ Login Page (Renders login.html)
@app.route("/login")
def login_page():
    return render_template("login.html")

# ✅ API Endpoint for Login Authentication
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email, password = data["email"], data["password"]
    
    if email in users and users[email] == password:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "❌ Invalid credentials. Try again."})

# ✅ Dashboard Route
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ✅ Outreach Mode Update API
@app.route("/update-mode", methods=["POST"])
def update_mode():
    data = request.json
    return jsonify({"message": f"Outreach mode updated to {data['mode']}!"})

# ✅ API to Fetch Leads (Fix: Matches `scraper.py`)
@app.route("/get-leads", methods=["GET"])
def get_leads():
    try:
        response = requests.get("http://127.0.0.1:5002/get-leads")  # ✅ Corrected from `get-clients`
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch leads: {str(e)}"}), 500

# ✅ API to Send Outreach (Emails, SMS, Calls)
@app.route("/send-outreach", methods=["POST"])
def send_outreach():
    data = request.json  # Receives { leads: [...], method: "email"/"sms"/"call", message: "..." }

    try:
        response = requests.post("http://127.0.0.1:5003/send-outreach", json=data)  # ✅ Corrected API call
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to send outreach: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
