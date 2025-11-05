from django.urls import path
from . import views

urlpatterns = [
    # Merchant
    path('merchant/add/', views.page_handler, {'template': 'easebuzz/merchant/add.html'}, name='merchant_add'),
    path('merchant/view/', views.page_handler, {'template': 'easebuzz/merchant/view.html'}, name='merchant_view'),
    path('merchant/stats/', views.page_handler, {'template': 'easebuzz/merchant/stats.html'}, name='merchant_stats'),
    path('merchant/service/', views.page_handler, {'template': 'easebuzz/merchant/service.html'}, name='merchant_service'),
    path('merchant/session/', views.page_handler, {'template': 'easebuzz/merchant/session.html'}, name='merchant_session'),
    path('merchant/currency/', views.page_handler, {'template': 'easebuzz/merchant/currency.html'}, name='merchant_currency'),
    path('merchant/bulksheets/', views.page_handler, {'template': 'easebuzz/merchant/bulksheets.html'}, name='merchant_bulksheets'),

    # Payout
    path('payout/dashboard/', views.page_handler, {'template': 'easebuzz/payout/dashboard.html'}, name='payout_dashboard'),
    path('payout/merchants/', views.page_handler, {'template': 'easebuzz/payout/merchants.html'}, name='payout_merchants'),
    path('payout/callback/', views.page_handler, {'template': 'easebuzz/payout/callback.html'}, name='payout_callback'),
    path('payout/wallet/', views.page_handler, {'template': 'easebuzz/payout/wallet.html'}, name='payout_wallet'),
    path('payout/ticket/', views.page_handler, {'template': 'easebuzz/payout/ticket.html'}, name='payout_ticket'),
    path('payout/currency/', views.page_handler, {'template': 'easebuzz/payout/currency.html'}, name='payout_currency'),
    path('payout/transaction/', views.page_handler, {'template': 'easebuzz/payout/transaction.html'}, name='payout_transaction'),
    path('payout/master_service/', views.page_handler, {'template': 'easebuzz/payout/master_service.html'}, name='payout_master_service'),
    path('payout/bulk_activities/', views.page_handler, {'template': 'easebuzz/payout/bulk_activities.html'}, name='payout_bulk'),

    # Payin
    path('payin/dashboard/', views.page_handler, {'template': 'easebuzz/payin/dashboard.html'}, name='payin_dashboard'),
    path('payin/method/', views.page_handler, {'template': 'easebuzz/payin/method.html'}, name='payin_method'),
    path('payin/merchants/', views.page_handler, {'template': 'easebuzz/payin/merchants.html'}, name='payin_merchants'),
    path('payin/request/', views.page_handler, {'template': 'easebuzz/payin/request.html'}, name='payin_request'),
    path('payin/routing/', views.page_handler, {'template': 'easebuzz/payin/routing.html'}, name='payin_routing'),
    path('payin/ticket/', views.page_handler, {'template': 'easebuzz/payin/ticket.html'}, name='payin_ticket'),
    path('payin/currency/', views.page_handler, {'template': 'easebuzz/payin/currency.html'}, name='payin_currency'),
    path('payin/callback_details/', views.page_handler, {'template': 'easebuzz/payin/callback_details.html'}, name='payin_callback_details'),
    path('payin/callback_gen/', views.page_handler, {'template': 'easebuzz/payin/callback_gen.html'}, name='payin_callback_gen'),
    path('payin/transaction/', views.page_handler, {'template': 'easebuzz/payin/transaction.html'}, name='payin_transaction'),
    path('payin/fuse/', views.page_handler, {'template': 'easebuzz/payin/fuse.html'}, name='payin_fuse'),
    path('payin/master_service/', views.page_handler, {'template': 'easebuzz/payin/master_service.html'}, name='payin_master_service'),
    path('payin/bulk_activities/', views.page_handler, {'template': 'easebuzz/payin/bulk_activities.html'}, name='payin_bulk'),

    # Product
    path('product/edit/', views.page_handler, {'template': 'easebuzz/product/edit.html'}, name='product_edit'),
    path('product/query/', views.page_handler, {'template': 'easebuzz/product/query.html'}, name='product_query'),
    path('product/transaction/', views.page_handler, {'template': 'easebuzz/product/transaction.html'}, name='product_transaction'),
]
