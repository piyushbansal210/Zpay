from django.urls import path
from . import views

urlpatterns = [
    path("add-merchant/", views.add_merchant, name="add-merchant"),
    path("list_merchants/", views.list_merchants, name="list_merchants"),
    path("update-merchant/", views.update_merchant, name="update-merchant"),
    path("merchant-stats/", views.merchant_stats, name="merchant-stats"),
    path("merchant/services/", views.merchant_services, name="merchant_services"),
    path("active_sessions/", views.active_sessions, name="active_sessions"),
    path("active_currency/", views.active_currency, name="active_currency"),
    path("all_bulk_sheets/",views.all_bulk_sheets, name="all_bulk_sheets"),

    path("payout_dashboard/", views.payout_dashboard_stats, name="payout_dashboard_stats"),
    path("easebuzz/payout_merchants/", views.payout_merchants_api, name="payout_merchants_api"),
    path("payout/callback_details/", views.get_payout_callback_details, name="payout-callback-details"),
]
