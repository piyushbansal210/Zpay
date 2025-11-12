# easebuzz/views.py
from django.http import Http404
from dashboard.utils import render_partial

ALLOWED = {
    'merchant': ['add','view','stats','service','session','currency','bulksheets'],
    'payout':   ['dashboard','merchants','callback','wallet','ticket','currency','payout_transaction'],
    'payin':    ['dashboard','method','merchants','request','routing','ticket','currency','callback_details','callback_gen'],
    'product':  ['edit','query','transaction'],
}

def section_page(request, section, page):
    section, page = section.lower(), page.lower()
    if section not in ALLOWED or page not in ALLOWED[section]: raise Http404()
    full = f"easebuzz/{section}/{page}.html"
    part = f"easebuzz/partials/{section}_{page}.html"
    return render_partial(request, full, part, {"title": f"{section} · {page}"})
