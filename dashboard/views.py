from .utils import render_partial

def home(request):
    return render_partial(
        request,
        "dashboard/pages/overview.html",       # for full page load
        "dashboard/partials/overview.html",    # for HTMX partial swap
        {}
    )

from .utils import render_partial

def easebuzz_dashboard(request):
    ctx = {
        "total_merchants": 120,
        "total_payins": 45000,
        "total_payouts": 38000,
        "total_volume": "₹9,80,40,000",
        "success_rate": "97.4%",
        "disputes": 32,
    }
    return render_partial(
        request,
        "dashboard/pages/easebuzz_home.html",
        "dashboard/partials/easebuzz_home.html",
        ctx
    )
