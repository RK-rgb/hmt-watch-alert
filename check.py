import requests
import os
from bs4 import BeautifulSoup

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

PRODUCTS = {
    "Quartz Maroon-Kohinoor": "https://www.hmtwatches.store/product/77733243-645c-4eac-8e69-63425e1cc09b",
    "Quartz Pink-Kohinoor": "https://www.hmtwatches.store/product/e1b512c1-35d7-4941-bc1d-c7e3f016de15",
    "Automatic Blue-Kohinoor": "https://www.hmtwatches.store/product/dc26b232-4231-4b58-bed5-984282684852",
    "Automatic Maroon-Kohinoor": "https://www.hmtwatches.store/product/79ec4cbd-d085-48a9-9127-7c0d583d45d6",
    "Automatic Yellow-Kohinoor": "https://www.hmtwatches.store/product/34aef933-9cb9-4a12-bbe3-7041e1c90677",
    "Automatic Yellow-Pink": "https://www.hmtwatches.store/product/fcd3bd02-1ee3-4ed4-8381-ca2cd2258139",
    "HMT Tareeq Quartz-Tiffany Blue": "https://www.hmtwatches.store/product/7281c42e-604a-4bd9-b011-066aa202eddd",
    
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
