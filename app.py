from flask import Flask, request
import os
import logging
import openai
from twilio.twiml.messaging_response import MessagingResponse

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask
app = Flask(__name__)
print("✅ Creating Flask app...")

# Load environment variables safely
try:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("Missing OPENAI_API_KEY")
except Exception as e:
    logging.error(f"❌ OpenAI key error: {e}")
    raise

@app.route("/", methods=["GET"])
def home():
    return "🏠 Hello from Railway!"

@app.route("/webhook", methods=["POST"])
def webhook():
    print("📨 /webhook route was hit!")
    try:
        incoming_msg = request.values.get("Body", "").strip()
        sender = request.values.get("From", "")
        print(f"📩 Message from {sender}: {incoming_msg}")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Ross's running coach. Be motivational, friendly, and helpful."},
                {"role": "user", "content": incoming_msg},
            ]
        )

        reply_text = response["choices"][0]["message"]["content"].strip()
        print(f"💬 Reply: {reply_text}")

    except Exception as e:
        logging.error(f"❌ Webhook error: {e}")
        reply_text = "Sorry Ross, I’m taking a nap 😴 Try again soon!"

    # Create Twilio WhatsApp reply
    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)
