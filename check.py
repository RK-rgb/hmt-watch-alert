from playwright.sync_api import sync_playwright
import requests
import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

PRODUCTS = {
    "Quartz Maroon - Kohinoor": "https://www.hmtwatches.store/product/77733243-645c-4eac-8e69-63425e1cc09b",
    "Quartz Pink - Kohinoor": "https://www.hmtwatches.store/product/e1b512c1-35d7-4941-bc1d-c7e3f016de15",
    "Automatic Blue - Kohinoor": "https://www.hmtwatches.store/product/dc26b232-4231-4b58-bed5-984282684852",
    "Automatic Maroon - Kohinoor": "https://www.hmtwatches.store/product/79ec4cbd-d085-48a9-9127-7c0d583d45d6",
    "Automatic Yellow - Kohinoor": "https://www.hmtwatches.store/product/34aef933-9cb9-4a12-bbe3-7041e1c90677",
    "Automatic Yellow - Pink": "https://www.hmtwatches.store/product/fcd3bd02-1ee3-4ed4-8381-ca2cd2258139",
    "HMT Tareeq Quartz - Tiffany Blue": "https://www.hmtwatches.store/product/7281c42e-604a-4bd9-b011-066aa202eddd",
    "HMT Janata Automatic - White": "https://www.hmtwatches.store/product/44333eb5-32ae-4189-85ab-209a8a451249",
    "HMT Stellar DASS 04 - Tiffany Blue": "https://www.hmtwatches.store/product/b8fbabdb-a49d-4e5d-92c6-71eda34c9382",
    "HMT Pilot Automatic Black": "https://www.hmtwatches.store/product/5cb806d1-3afa-4511-80b4-49e457c1cbab"
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

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=True
    )

    page = browser.new_page()

    for name, url in PRODUCTS.items():

        try:

            page.goto(
                url,
                wait_until="networkidle",
                timeout=60000
            )

            page.wait_for_timeout(3000)

            buttons = page.locator("button").all_text_contents()

            print(f"{name}: {buttons}")

            buttons = [b.strip().lower() for b in buttons]

            add_to_cart = "add to cart" in buttons
            buy_now = "buy now" in buttons

            in_stock = add_to_cart and buy_now

            print(
                f"{name}: "
                f"add_to_cart={add_to_cart}, "
                f"buy_now={buy_now}"
            )

            if in_stock:

                send_telegram(
                    f"🚨 HMT WATCH AVAILABLE 🚨\n\n{name}\n\n{url}"
                )

                print(f"{name}: AVAILABLE")

            else:

                print(f"{name}: Out of Stock")

        except Exception as e:

            print(f"{name}: ERROR - {e}")

    browser.close()
