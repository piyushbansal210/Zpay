# easebuzz/urls.py
from django.urls import path
from . import views
urlpatterns = [
    path('merchant/<slug:page>/', views.section_page, {'section': 'merchant'}),
    path('payout/<slug:page>/',   views.section_page, {'section': 'payout'}),
    path('payin/<slug:page>/',    views.section_page, {'section': 'payin'}),
    path('product/<slug:page>/',  views.section_page, {'section': 'product'}),
]
