import os
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print(f"Token present: {bool(TOKEN)}")
print(f"Chat ID present: {bool(CHAT_ID)}")

if not TOKEN or not CHAT_ID:
    raise SystemExit("Missing TELEGRAM_TOKEN or CHAT_ID secret")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {
    "chat_id": CHAT_ID,
    "text": "✅ Bot is working! Your SportyBet automation is live.\n\nNext: I'll send picks every 5 hours."
}

r = requests.post(url, data=data, timeout=10)
print("Status:", r.status_code)
print("Response:", r.text)

if r.status_code != 200:
    raise SystemExit(f"Telegram error: {r.text}")
