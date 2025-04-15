from flask import Flask, request
import os
import openai
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def health_check():
    return "Ross AI Coach is running! 🧠✅"


@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    print(f"📩 Message from {sender}: {incoming_msg}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Ross's running coach. Be motivational, friendly, and helpful."},
                {"role": "user", "content": incoming_msg}
            ]
        )
        reply_text = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        reply_text = "Sorry Ross, I'm taking a nap 😴 Try again soon!"

    resp = MessagingResponse()
    resp.message(reply_text)
    return str(resp)

#if __name__ == "__main__":
  #  app.run(host="0.0.0.0", port=5000)
