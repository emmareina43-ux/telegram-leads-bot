import requests
from flask import Flask, request

app = Flask(__name__)

TELEGRAM_TOKEN = "8392567454:AAERXi9efycfhudrw340ofi04st6Dfcnt9A"   # <-- pune tokenul REAL aici
CHAT_ID = "716093979"  # chat id-ul tau

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

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
