import os
import logging
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask
logging.info("✅ Creating Flask app...")
app = Flask(__name__)
logging.info("✅ Flask app instance created")

# Initialize OpenAI client
client = OpenAI()

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")
    logging.info(f"📩 Message from {sender}: {incoming_msg}")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Ross's running coach. Be motivational, friendly, and helpful."},
                {"role": "user", "content": incoming_msg},
            ]
        )
        reply_text = response.choices[0].message.content.strip()
        logging.info(f"✅ Reply: {reply_text}")

    except Exception as e:
        logging.error(f"⚠️ OpenAI error: {e}")
        reply_text = "Sorry Ross, I'm taking a nap 😴 Try again soon!"

    # Create Twilio WhatsApp reply
    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)
