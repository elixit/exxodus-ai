import stripe
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template

# Load Stripe API keys from .env
load_dotenv()
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")

stripe.api_key = STRIPE_SECRET_KEY

app = Flask(__name__, template_folder="../frontend/templates")

# ✅ Home route - serves the payment page
@app.route("/")
def home():
    return render_template("payment.html")

# ✅ Stripe Checkout session creation
@app.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "AI Lead Generation - Unlimited Plan",
                        "description": "🚀 Unlimited AI-powered lead generation with email, SMS & cold call automation."
                    },
                    "unit_amount": 19900,  # $199.00 per month
                    "recurring": {"interval": "month"}
                },
                "quantity": 1,
            }],
            success_url="http://127.0.0.1:5002/payment-success",
            cancel_url="http://127.0.0.1:5002/payment-failed",
        )
        return jsonify({"checkout_url": session.url})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ✅ Payment success page
@app.route("/payment-success")
def payment_success():
    return render_template("success.html")  # Make sure success.html exists

# ✅ Payment failed page
@app.route("/payment-failed")
def payment_failed():
    return "❌ Payment Failed. Please try again."

if __name__ == "__main__":
    app.run(debug=True, port=5002)
