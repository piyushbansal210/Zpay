# jiopay/views.py
from django.http import Http404
from dashboard.utils import render_partial

ALLOWED = {
    'merchant': [
        'add', 'view', 'stats', 'service', 'session', 'currency', 'bulksheets'
    ],
    'payout': [
        'dashboard', 'merchants', 'callback', 'wallet', 'ticket', 'currency',
        # transaction group
        'payout_transaction', 'payout_transaction_request_history',
        'payout_transaction_virtual', 'payout_transaction_acquirer_report',
        # master service group
        'payout_master_add_account', 'payout_master_activate_account',
        'payout_master_bank_statements', 'payout_master_balance_list',
        # bulk group
        'payout_bulk_update', 'payout_bulk_txn_data'
    ],
    'payin': [
        'dashboard', 'method', 'merchants', 'request', 'routing', 'ticket',
        'currency', 'callback_details', 'callback_gen',
        # transaction group
        'payin_transaction', 'payin_transaction_dispute',
        'payin_transaction_chargeback', 'payin_transaction_flag',
        'payin_transaction_virtual', 'payin_transaction_unmatched',
        'payin_transaction_acquirer_report',
        # fuse group
        'payin_fuse_fraud_list', 'payin_fuse_fraud_upload',
        # master group
        'payin_master_add_mid', 'payin_master_activate_mid',
        'payin_master_upi_handler', 'payin_master_gateway',
        # bulk group
        'payin_bulk_dispute', 'payin_bulk_update', 'payin_bulk_chargeback',
        'payin_bulk_bank_txn', 'payin_bulk_get_request',
        'payin_bulk_resend_callback', 'payin_bulk_resend_bank_callback'
    ],
    'product': [
        'edit', 'query', 'transaction'
    ],
}


def section_page(request, section, page):
    """
    Dynamically render any allowed JioPay section/page pair
    """
    section, page = section.lower(), page.lower()
    if section not in ALLOWED or page not in ALLOWED[section]:
        raise Http404(f"Invalid section or page: {section}/{page}")

    full_template = f"jiopay/{section}/{page}.html"
    partial_template = f"jiopay/partials/{section}_{page}.html"
    ctx = {"title": f"{section.title()} · {page.replace('_', ' ').title()}"}

    return render_partial(request, full_template, partial_template, ctx)
