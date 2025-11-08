from .utils import render_partial

def home(request):
    ctx = {"total_merchants": 12, "total_payins": 540, "total_payouts": 480, "total_volume": "₹24,50,000"}
    return render_partial(request, "dashboard/pages/home.html", "dashboard/partials/home.html", ctx)
