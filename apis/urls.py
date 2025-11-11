from django.urls import path
from . import views

urlpatterns = [
    path("add-merchant/", views.add_merchant, name="add-merchant"),
    path("list-merchants/", views.list_merchants, name="list-merchants"),
    path("update-merchant/", views.update_merchant, name="update-merchant"),
    path("merchant-stats/", views.merchant_stats, name="merchant-stats"),
]
