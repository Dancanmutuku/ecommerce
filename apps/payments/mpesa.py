import requests
import base64
from datetime import datetime
from decouple import config


# === MPESA CONFIGURATION ===
MPESA_CONSUMER_KEY = config("MPESA_CONSUMER_KEY")
MPESA_CONSUMER_SECRET = config("MPESA_CONSUMER_SECRET")
SHORTCODE = config("MPESA_SHORTCODE")
PASSKEY = config("MPESA_PASSKEY")
CALLBACK_URL = config("MPESA_CALLBACK_URL")

def get_access_token():
    auth = base64.b64encode(
        f"{MPESA_CONSUMER_KEY}:{MPESA_CONSUMER_SECRET}".encode()
    ).decode()

    response = requests.get(
        "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
        headers={"Authorization": f"Basic {auth}"},
        timeout=30,
    )

    response.raise_for_status()
    return response.json()["access_token"]


def stk_push(phone, amount, order_id):
    access_token = get_access_token()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    password = base64.b64encode(
        f"{SHORTCODE}{PASSKEY}{timestamp}".encode()
    ).decode()

    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": str(order_id),
        "TransactionDesc": "Order Payment",
    }

    response = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )

    response.raise_for_status()
    return response.json()
