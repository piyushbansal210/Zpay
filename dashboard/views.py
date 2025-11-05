from django.shortcuts import render

def index(request):
    stats = {
        "total_merchants": 12,
        "total_payins": 540,
        "total_payouts": 480,
        "total_volume": "₹24,50,000"
    }
    providers = ["Razorpay", "PayU", "Stripe"]
    return render(request, 'dashboard/index.html', {"stats": stats, "providers": providers})

