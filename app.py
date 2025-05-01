from flask import Flask, request
import os
import logging
import openai
from twilio.twiml.messaging_response import MessagingResponse

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask
app = Flask(__name__)

# Load environment variables safely
try:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("Missing OPENAI_API_KEY")
except Exception as e:
    logging.error(f"❌ OpenAI key error: {e}")
    raise

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
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply_text = response["choices"][0]["message"]["content"].strip()
        logging.info(f"✅ Reply: {reply_text}")

    except Exception as e:
        logging.error(f"🚫 OpenAI error: {e}")
        reply_text = "Sorry Ross, I'm taking a nap 😴 Try again soon!"

    # Create Twilio WhatsApp reply
    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)

# Commented out for Gunicorn
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
