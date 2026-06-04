import requests
import json
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

PRODUCTS = {
    "Maroon":
    "https://www.hmtwatches.store/product/77733243-645c-4eac-8e69-63425e1cc09b",

    "Pink":
    "https://www.hmtwatches.store/product/e1b512c1-35d7-4941-bc1d-c7e3f016de15"
}

STATE_FILE = "state.json"


def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        }
    )


try:
    with open(STATE_FILE) as f:
        state = json.load(f)
except:
    state = {}


for name, url in PRODUCTS.items():

    page = requests.get(
        url,
        headers={
            "User-Agent":
            "Mozilla/5.0"
        },
        timeout=20
    )

    text = page.text.lower()

    in_stock = (
        "out of stock" not in text
    )

    previous = state.get(name, False)

    if in_stock and not previous:

        send_telegram(
            f"🚨 HMT Kohinoor {name} is AVAILABLE!\n{url}"
        )

    state[name] = in_stock


with open(STATE_FILE, "w") as f:
    json.dump(state, f)
