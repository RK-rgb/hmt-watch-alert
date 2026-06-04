import requests
import os
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

PRODUCTS = {
    "Maroon": "https://www.hmtwatches.store/product/77733243-645c-4eac-8e69-63425e1cc09b",
    "Pink": "https://www.hmtwatches.store/product/e1b512c1-35d7-4941-bc1d-c7e3f016de15"
}

def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": msg
        },
        timeout=20
    )

for name, url in PRODUCTS.items():

    try:
        page = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=20
        )

        soup = BeautifulSoup(page.text, "html.parser")

        out_of_stock = False

        for button in soup.find_all("button"):
            text = button.get_text(strip=True).lower()

            if text == "out of stock":
                out_of_stock = True
                break

        if not out_of_stock:
            send_telegram(
                f"🚨 HMT Kohinoor {name} AVAILABLE!\n{url}"
            )
            print(f"{name}: AVAILABLE")

        else:
            print(f"{name}: Out of Stock")

    except Exception as e:
        print(f"{name}: ERROR - {e}")
