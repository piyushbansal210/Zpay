import hashlib
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# ==============================
# CONFIGURATION
# ==============================

EASEBUZZ_KEY = "3GEV07NS8T"
EASEBUZZ_SALT = "4C486ZG6LO"
EASEBUZZ_BASE_URL = "https://dashboard.easebuzz.in/partner/v1"

# ==============================
# UTILITY FUNCTIONS
# ==============================

def generate_hash(values, ordered_keys):
    """
    Generate SHA512 hash of all payload values in a fixed order + salt.
    Used when specific hash ordering is required by Easebuzz API.
    """
    data_string = "|".join(str(values.get(k, "")) for k in ordered_keys) + "|" + EASEBUZZ_SALT
    return hashlib.sha512(data_string.encode()).hexdigest().upper()

def simple_hash(key, salt):
    """
    Simple hash for authentication: SHA512(key|salt).
    Used for standard endpoints (e.g. merchant_list).
    """
    return hashlib.sha512(f"{key}|{salt}".encode()).hexdigest().upper()

def make_request(url, payload, method="POST", headers=None):
    """
    Centralized Easebuzz API request handler with error handling.
    """
    try:
        if headers is None:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
        if method == "GET":
            response = requests.get(url, params=payload, timeout=20)
        else:
            response = requests.post(url, data=payload, headers=headers, timeout=20)
        try:
            return response.json(), response.status_code
        except Exception:
            return {"raw_response": response.text}, response.status_code
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}, status.HTTP_503_SERVICE_UNAVAILABLE

# ==============================
# ADD MERCHANT (Sub-merchant Onboarding)
# ==============================

@api_view(["POST"])
def add_merchant(request):
    """
    Onboard a new sub-merchant under your Easebuzz aggregator account.
    POST with all required fields.
    """
    try:
        data = request.data
        required_fields = [
            "merchant_name", "email", "phone", "business_type", "pan", "gstin",
            "address", "city", "state", "pincode", "bank_name", "account_no", "ifsc_code"
        ]
        payload = {"key": EASEBUZZ_KEY}
        for field in required_fields:
            value = data.get(field)
            if not value:
                return Response({"error": f"Missing required field: {field}"}, status=status.HTTP_400_BAD_REQUEST)
            payload[field] = value
        # Hash generation (order matters)
        payload["hash"] = generate_hash(payload, required_fields)
        url = f"{EASEBUZZ_BASE_URL}/merchant_onboard"
        result, status_code = make_request(url, payload, "POST")
        return Response(result, status=status_code)
    except Exception as e:
        print("Error in add_merchant:", str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ==============================
# LIST MERCHANTS
# ==============================

@api_view(["GET"])
def list_merchants(request):
    """
    Fetch all merchants/sub-merchants onboarded under your Easebuzz partner account.
    Uses GET with key/hash.
    """
    try:
        payload = {
            "key": EASEBUZZ_KEY,
            "hash": simple_hash(EASEBUZZ_KEY, EASEBUZZ_SALT)
        }
        url = f"{EASEBUZZ_BASE_URL}/merchant_list"
        result, status_code = make_request(url, payload, "GET")
        return Response(result, status=status_code)
    except Exception as e:
        print("Error in list_merchants:", str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ==============================
# UPDATE MERCHANT
# ==============================

@api_view(["POST"])
def update_merchant(request):
    """
    Update an existing merchant's details.
    POST with sub_merchant_key and any optional fields to update.
    """
    try:
        data = request.data
        sub_merchant_key = data.get("sub_merchant_key")
        if not sub_merchant_key:
            return Response({"error": "sub_merchant_key is required"}, status=status.HTTP_400_BAD_REQUEST)
        payload = {"key": EASEBUZZ_KEY, "sub_merchant_key": sub_merchant_key}
        # Optional fields
        optional_fields = [
            "merchant_name", "email", "phone", "address", "city", "state", "pincode",
            "business_type", "gstin", "pan"
        ]
        for field in optional_fields:
            if data.get(field):
                payload[field] = data[field]
        payload["hash"] = simple_hash(EASEBUZZ_KEY, EASEBUZZ_SALT)
        url = f"{EASEBUZZ_BASE_URL}/merchant_update"
        result, status_code = make_request(url, payload, "POST")
        return Response(result, status=status_code)
    except Exception as e:
        print("Error in update_merchant:", str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ==============================
# ENDPOINT EXAMPLES
# ==============================
# POST /add_merchant/         --> Submerchant onboarding
# GET /list_merchants/        --> List all (sub)merchants
# POST /update_merchant/      --> Update merchant data




import hashlib
import requests
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# ==============================
# CONFIGURATION
# ==============================

EASEBUZZ_KEY = "3GEV07NS8T"
EASEBUZZ_SALT = "4C486ZG6LO"
EASEBUZZ_BASE_URL = "https://dashboard.easebuzz.in/partner/v1"
TXN_REPORT_ENDPOINT = f"{EASEBUZZ_BASE_URL}/transaction_report"  # Replace with the correct endpoint if available


# ==============================
# UTILS
# ==============================

def simple_hash(key, salt):
    """Simple SHA512 hash for Easebuzz authentication."""
    return hashlib.sha512(f"{key}|{salt}".encode()).hexdigest().upper()


def mk_request(url, payload, method="POST", headers=None):
    """Handle GET or POST requests with standard headers and timeout."""
    if headers is None:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        if method == "GET":
            response = requests.get(url, params=payload, timeout=20)
        else:
            response = requests.post(url, data=payload, headers=headers, timeout=20)

        try:
            return response.json(), response.status_code
        except Exception:
            return {"raw_response": response.text}, response.status_code
    except Exception as e:
        return {"error": str(e)}, 503


# ==============================
# MERCHANT STATS API
# ==============================

@api_view(["GET"])
def merchant_stats(request):
    """
    Fetch statistics for all Easebuzz merchants between `from_date` and `to_date`.
    """
    try:
        # Parse date range or set defaults
        to_date = request.GET.get("to_date") or datetime.now().strftime("%Y-%m-%d")
        from_date = request.GET.get("from_date") or (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        # Step 1: Fetch merchants
        merchant_payload = {
            "key": EASEBUZZ_KEY,
            "hash": simple_hash(EASEBUZZ_KEY, EASEBUZZ_SALT),
        }
        merchant_url = f"{EASEBUZZ_BASE_URL}/merchant_list"
        merchants_data, merchant_status = mk_request(merchant_url, merchant_payload, "POST")

        merchants = merchants_data.get("merchants", []) if isinstance(merchants_data, dict) else []
        all_stats = []

        # Step 2: Fetch stats per merchant
        for merchant in merchants:
            merchant_key = merchant.get("merchant_key")
            business_name = merchant.get("merchant_name")

            txn_payload = {
                "key": EASEBUZZ_KEY,
                "sub_merchant_key": merchant_key,
                "from_date": from_date,
                "to_date": to_date,
                "hash": simple_hash(EASEBUZZ_KEY, EASEBUZZ_SALT),
            }

            stats_data, stats_status = mk_request(TXN_REPORT_ENDPOINT, txn_payload, "POST")

            stat_entry = {
                "merchant_name": business_name,
                "merchant_key": merchant_key,
                "value_payout": stats_data.get("payout_amount", 0),
                "num_payout": stats_data.get("payout_count", 0),
                "value_payin": stats_data.get("payin_amount", 0),
                "num_payin": stats_data.get("payin_count", 0),
                "currency": stats_data.get("currency", "INR"),
            }
            all_stats.append(stat_entry)

        return Response(
            {
                "status": 1,
                "from_date": from_date,
                "to_date": to_date,
                "total_merchants": len(all_stats),
                "data": all_stats,
            },
            status=status.HTTP_200_OK,
        )

    except Exception as e:
        print("Error in merchant_stats:", str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
