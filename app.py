from flask import Flask, request
import os
import logging
import openai
from twilio.twiml.messaging_response import MessagingResponse

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask
app = Flask(__name__)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Root route to show app is running
@app.route("/")
def index():
    return "Running Coach API is live!"

# Webhook for WhatsApp
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")
    logging.info(f"📩 Message from {sender}: {incoming_msg}")

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Ross's running coach. Be motivational, friendly, and helpful."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply_text = response.choices[0].message.content.strip()
        logging.info(f"✅ Reply: {reply_text}")

    except Exception as e:
        logging.error(f"⚠️ OpenAI error: {e}")
        reply_text = "Sorry Ross, I'm taking a nap 😴 Try again soon!"

    # Return Twilio WhatsApp response
    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)

# For Gunicorn compatibility
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
