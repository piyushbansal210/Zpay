import hashlib
import requests
import json
from django.conf import settings

EASEBUZZ_KEY = getattr(settings, "EASEBUZZ_KEY", "")
EASEBUZZ_SALT = getattr(settings, "EASEBUZZ_SALT", "")
EASEBUZZ_BASE_URL = "https://dashboard.easebuzz.in/partner/v1"  # change if sandbox/live differs

def generate_hash(payload):
    """Generate SHA512 hash required by Easebuzz."""
    raw_string = '|'.join(str(payload[k]) for k in sorted(payload.keys())) + '|' + EASEBUZZ_SALT
    return hashlib.sha512(raw_string.encode()).hexdigest()


def add_merchant_to_easebuzz(data):
    url = f"{EASEBUZZ_BASE_URL}/merchant_onboard"
    payload = {
        "key": EASEBUZZ_KEY,
        "merchant_name": data.get("merchant_name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "business_type": data.get("business_type", "IT Services"),
    }
    payload["hash"] = generate_hash(payload)

    response = requests.post(url, data=payload)
    return response.json()


def get_merchant_list():
    url = f"{EASEBUZZ_BASE_URL}/merchant_list"
    payload = {
        "key": EASEBUZZ_KEY,
    }
    payload["hash"] = generate_hash(payload)

    response = requests.post(url, data=payload)
    return response.json()
