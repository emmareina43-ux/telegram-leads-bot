import requests
from flask import Flask, request

app = Flask(__name__)

# 🔥 Pune tokenul TAU aici (doar tu îl vezi)
TELEGRAM_TOKEN = "8392567454:AAERXi9efycfhudrw340ofi04st6Dfcnt9A"

# 🔥 Chat ID-ul tau
CHAT_ID = "716093979"

# 🔥 Verify token-ul pe care îl pui SI in Facebook Webhooks
VERIFY_TOKEN = "beezpixel123"

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

# ✔ Facebook verifică webhook-ul prin GET — asta era lipsă
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Verification token mismatch", 403

# ✔ Facebook trimite leadurile prin POST
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    
    field_data = data.get("leadgen_field_data", [])

    def get_value(index):
        try:
            return field_data[index]["values"][0]
        except:
            return "N/A"

    name = get_value(0)
    phone = get_value(1)
    email = get_value(2)

    message = f"""
<b>🚀 Lead nou!</b>

<b>Nume:</b> {name}
<b>Telefon:</b> {phone}
<b>Email:</b> {email}
"""

    send_message(message)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
