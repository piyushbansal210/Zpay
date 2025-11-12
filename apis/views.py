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

# @api_view(["GET"])
# def list_merchants(request):
#     """
#     Fetch all merchants/sub-merchants onboarded under your Easebuzz partner account.
#     Uses GET with key/hash.
#     """
#     try:
#         payload = {
#             "key": EASEBUZZ_KEY,
#             "hash": simple_hash(EASEBUZZ_KEY, EASEBUZZ_SALT)
#         }
#         url = f"{EASEBUZZ_BASE_URL}/merchant_list"
#         result, status_code = make_request(url, payload, "GET")
#         return Response(result, status=status_code)
#     except Exception as e:
#         print("Error in list_merchants:", str(e))
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@api_view(["POST"])
def merchant_services(request):
    """
    Fetch all active/inactive services (Auth, Payin, Payout, etc.)
    for a given merchant from Easebuzz.
    """
    try:
        merchant_key = request.data.get("sub_merchant_key")
        if not merchant_key:
            return Response({"error": "sub_merchant_key is required"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            "key": EASEBUZZ_KEY,
            "sub_merchant_key": merchant_key,
            "hash": simple_hash(EASEBUZZ_KEY, EASEBUZZ_SALT),
        }

        # ==============================
        # Option A: Partner API (Recommended)
        # ==============================
        url = f"{EASEBUZZ_BASE_URL}/merchant_service_list"

        # ==============================
        # Option B: If A doesn't exist in your version
        # Replace with the direct dashboard API:
        # url = "https://dashboard.easebuzz.in/api/service/list"
        # payload["merchant_email"] = request.data.get("merchant_email")
        # ==============================

        result, status_code = make_request(url, payload, "POST")

        # Normalize data
        if isinstance(result, dict) and result.get("status") in [1, "1", "success"]:
            services = result.get("data", {}).get("services", [])
            return Response({"merchant": merchant_key, "services": services}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"merchant": merchant_key, "error": result.get("message", "No data found")},
                status=status.HTTP_404_NOT_FOUND,
            )

    except Exception as e:
        print("Error in merchant_services:", str(e))
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
import hashlib


@api_view(["GET"])
def active_sessions(request):
    """
    Fetch active merchant sessions from Easebuzz.
    """
    try:
        payload = {
            "key": EASEBUZZ_KEY,
            "hash": simple_hash(EASEBUZZ_KEY, EASEBUZZ_SALT),
        }
        url = f"{EASEBUZZ_BASE_URL}/merchant_active_session"
        response = requests.post(url, data=payload, timeout=15)

        if response.status_code == 200:
            data = response.json()
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to fetch sessions"}, status=response.status_code)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


import hashlib
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status



@api_view(["GET"])
def active_currency(request):
    """
    Fetch all active currencies for your partner/merchant account from Easebuzz.
    """
    try:
        payload = {
            "key": EASEBUZZ_KEY,
            "hash": hashlib.sha512(f"{EASEBUZZ_KEY}|{EASEBUZZ_SALT}".encode()).hexdigest().upper(),
        }

        url = f"{EASEBUZZ_BASE_URL}/merchant_active_currency"
        response = requests.post(url, data=payload, timeout=20)
        data = response.json()

        # API success
        if isinstance(data, dict) and data.get("status") in [1, "1", "success"]:
            return Response({"currencies": data.get("data", [])}, status=status.HTTP_200_OK)

        # API fallback (no data)
        return Response(
            {"currencies": [], "message": data.get("message", "No active currencies found")},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        print("Error in active_currency:", str(e))
        return Response({"currencies": [], "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



import hashlib
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["GET"])
def all_bulk_sheets(request):
    try:
        payload = {
            "key": EASEBUZZ_KEY,
            "hash": hashlib.sha512(f"{EASEBUZZ_KEY}|{EASEBUZZ_SALT}".encode()).hexdigest().upper(),
        }

        url = f"{EASEBUZZ_BASE_URL}/bulk_sheet_list"
        response = requests.post(url, data=payload, timeout=25)
        data = response.json()

        if isinstance(data, dict) and data.get("status") in [1, "1", "success"]:
            return Response({"sheets": data.get("data", [])}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"sheets": [], "message": data.get("message", "No bulk sheets found")},
                status=status.HTTP_200_OK
            )
    except Exception as e:
        print("Error in all_bulk_sheets:", str(e))
        return Response({"sheets": [], "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


import hashlib
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(["GET"])
def list_merchants(request):
    """
    Fetch all merchants from Easebuzz partner account
    """
    try:
        payload = {
            "key": EASEBUZZ_KEY,
            "hash": hashlib.sha512(f"{EASEBUZZ_KEY}|{EASEBUZZ_SALT}".encode()).hexdigest().upper(),
        }

        url = f"{EASEBUZZ_BASE_URL}/merchant_list"
        response = requests.post(url, data=payload, timeout=20)
        data = response.json()

        if isinstance(data, dict) and data.get("status") in ["1", 1, "success"]:
            merchants = data.get("data", [])
            return Response({"merchants": merchants}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"merchants": [], "message": data.get("message", "No merchants found")},
                status=status.HTTP_200_OK
            )

    except Exception as e:
        print("Error fetching merchant list:", str(e))
        return Response({"merchants": [], "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


import hashlib, requests
from datetime import datetime, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def make_request(url, payload):
    try:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(url, data=payload, headers=headers, timeout=20)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500


@api_view(["GET"])
def payout_dashboard_stats(request):
    try:
        payload = {"key": EASEBUZZ_KEY, "hash": simple_hash(EASEBUZZ_KEY, EASEBUZZ_SALT)}
        url = f"{EASEBUZZ_BASE_URL}/payout_overview"
        data, code = make_request(url, payload)

        # Simulated / fallback structure
        fallback_summary = {
            "pending": 0,
            "initiated": 0,
            "success": 0,
            "failed": 0,
            "refunded": 0,
            "total": 0,
        }

        stats = {
            "active_merchants": data.get("active_merchants", 0),
            "wallet_balance": float(data.get("wallet_balance", 0)),
            "routes": data.get("routes", []),
            "graph": data.get("graph", []),
            "summary": data.get("summary", fallback_summary),
        }

        return Response({"status": 1, "data": stats}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from easebuzz.models import Merchant


@api_view(["GET"])
def payout_merchants_api(request):
    """
    Fetch all payout merchants dynamically.
    Optional search: /api/easebuzz/payout_merchants/?q=<query>
    """
    try:
        query = request.GET.get("q", "").strip()

        merchants = Merchant.objects.all().order_by("business_name")
        if query:
            merchants = merchants.filter(
                Q(business_name__icontains=query) |
                Q(email__icontains=query) |
                Q(mobile_no__icontains=query)
            )

        data = [
            {
                "business_name": m.business_name,
                "mobile_no": m.mobile_no or "",
                "email": m.email or "",
                "inr_balance": float(m.inr_balance or 0),
                "hold_balance": float(m.hold_balance or 0),
                "prepaid_status": m.prepaid_status or "Inactive",
            }
            for m in merchants
        ]

        return Response(
            {"status": 1, "count": len(data), "merchants": data},
            status=status.HTTP_200_OK
        )

    except Exception as e:
        print("❌ payout_merchants_api error:", e)
        return Response(
            {"status": 0, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )



import hashlib
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# ==============================
# CALLBACK DETAILS
# ==============================

@api_view(["GET"])
def get_payout_callback_details(request):
    """
    Fetch payout callback details from Easebuzz.
    Optional: ?pg_ref=<pg_ref>
    """
    try:
        pg_ref = request.GET.get("pg_ref", "")

        payload = {
            "key": EASEBUZZ_KEY,
            "hash": hashlib.sha512(f"{EASEBUZZ_KEY}|{EASEBUZZ_SALT}".encode()).hexdigest().upper(),
        }

        if pg_ref:
            payload["pg_ref"] = pg_ref

        # Official Easebuzz API for callback details
        url = f"{EASEBUZZ_BASE_URL}/payout_callback_details"

        response = requests.post(url, data=payload, timeout=25)
        data = response.json()

        # Normalize output
        if isinstance(data, dict) and data.get("status") in ["1", 1, "success"]:
            callbacks = data.get("data", [])
            return Response({"status": 1, "callbacks": callbacks}, status=status.HTTP_200_OK)
        else:
            return Response(
                {
                    "status": 0,
                    "callbacks": [],
                    "message": data.get("message", "No callback data found"),
                },
                status=status.HTTP_200_OK,
            )

    except Exception as e:
        print("❌ Error in get_payout_callback_details:", str(e))
        return Response({"status": 0, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
