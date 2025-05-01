from flask import Flask, request
import os
import logging
import openai
from twilio.twiml.messaging_response import MessagingResponse

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logging.info("✅ Creating Flask app...")

# Initialize Flask
app = Flask(__name__)
logging.info("✅ Flask app instance created")

# Root route for Railway health check
@app.route("/", methods=["GET"])
def home():
    return "AI Running Coach is live!", 200

# Webhook route for WhatsApp
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    logging.info(f"📩 Message from {sender}: {incoming_msg}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Ross's running coach. Be motivational, friendly, and helpful."},
                {"role": "user", "content": incoming_msg},
            ]
        )
        reply_text = response["choices"][0]["message"]["content"].strip()
        logging.info(f"✅ Reply: {reply_text}")

   except Exception as e:
    logging.exception("❌ OpenAI API call failed:")
    reply_text = "Sorry Ross, I'm taking a nap 😴 Try again soon!"

    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)
