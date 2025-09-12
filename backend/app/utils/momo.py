import uuid
import requests
import hmac
import hashlib
import time

# ========== CONFIG ==========
ENDPOINT = "https://test-payment.momo.vn/v2/gateway/api/create"
ACCESS_KEY = "F8BBA842ECF85"
SECRET_KEY = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
PARTNER_CODE = "MOMO"
IPN_URL = "https://webhook.site/b3088a6a-2d17-4f8d-a383-71389a6c600b"
PARTNER_NAME = "MoMo Payment"
STORE_ID = "Test Store"
LANG = "vi"


def generate_signature(
    order_id, request_id, amount, redirect_url, request_type="captureWallet"
):
    """Tạo chữ ký HMAC SHA256"""
    raw_signature = (
        f"accessKey={ACCESS_KEY}"
        f"&amount={amount}"
        f"&extraData="
        f"&ipnUrl={IPN_URL}"
        f"&orderId={order_id}"
        f"&orderInfo=Thanh toan don hang {order_id}"
        f"&partnerCode={PARTNER_CODE}"
        f"&redirectUrl={redirect_url}"
        f"&requestId={request_id}"
        f"&requestType={request_type}"
    )

    h = hmac.new(
        SECRET_KEY.encode("utf-8"), raw_signature.encode("utf-8"), hashlib.sha256
    )
    return h.hexdigest()


def build_request_data(
    order_id, request_id, amount, redirect_url, signature, request_type="captureWallet"
):
    """Tạo payload JSON gửi MoMo"""
    return {
        "partnerCode": PARTNER_CODE,
        "orderId": order_id,
        "partnerName": PARTNER_NAME,
        "storeId": STORE_ID,
        "ipnUrl": IPN_URL,
        "amount": amount,
        "lang": LANG,
        "requestType": request_type,
        "redirectUrl": redirect_url,
        "orderInfo": f"Thanh toan don hang {order_id}",
        "requestId": request_id,
        "extraData": "",
        "signature": signature,
    }


def create_payment(order_id: str, amount: str, return_url: str):
    """Tạo thanh toán với MoMo"""
    request_id = str(uuid.uuid4())

    # Đảm bảo orderId là unique
    unique_order_id = f"{order_id}_{int(time.time())}"

    amount = str(int(float(amount)))
    signature = generate_signature(unique_order_id, request_id, amount, return_url)

    payload = build_request_data(
        unique_order_id, request_id, amount, return_url, signature
    )

    response = requests.post(
        ENDPOINT, json=payload, headers={"Content-Type": "application/json"}
    )
    return response.json()
