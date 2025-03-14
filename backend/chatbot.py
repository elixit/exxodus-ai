from flask import Flask, request, jsonify, render_template
from together import Together
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Initialize Together.AI client
client = Together(api_key=TOGETHER_API_KEY)

app = Flask(__name__, template_folder="../frontend/templates")

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"response": "Please enter a message."})

    try:
        # Together.AI API Call using a 100% Free Model
        response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.1",  # ✅ Free model
            messages=[{"role": "user", "content": user_message}]
        )

        # ✅ Correctly extract response message
        ai_response = response.choices[0].message.content

        return jsonify({"response": ai_response})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True, port=5001)
