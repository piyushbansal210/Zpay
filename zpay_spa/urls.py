# zpay_spa/urls.py - UNIFIED LOGIN VERSION

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

# Import the unified login view
# Option 1: If you added it to views_auth.py
from dashboard.views_auth import unified_login_view, unified_logout_view

# Option 2: If you created unified_auth.py
# from dashboard.unified_auth import unified_login_view, unified_logout_view

# Import chat views for merchant routes
from dashboard import chat_views

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # UNIFIED LOGIN (Single login for everyone)
    path('login/', unified_login_view, name='login'),
    path('logout/', unified_logout_view, name='logout'),
    
    # Backward compatibility (redirect old URLs to new unified login)
    path('auth/login/', lambda request: redirect('/login/')),
    path('merchant/login/', lambda request: redirect('/login/')),
    
    # Dashboard routes (for admin users)
    path('dashboard/', include('dashboard.urls')),
    
    # Auth routes (keep for other auth-related pages if any)
    path('auth/', include('dashboard.auth_urls')),
    
    # Easebuzz routes
    path('easebuzz/', include('easebuzz.urls')),
    path('jiopay/', include('jiopay.urls')),
    
    # API routes
    path('api/', include('apis.urls')),
    
    # Merchant routes (for merchant-specific pages)
    path('merchant/logout/', lambda request: redirect('/logout/')),  # Redirect to unified logout
    path('merchant/dashboard/', chat_views.merchant_dashboard, name='merchant_dashboard'),
    path('merchant/chat/', chat_views.merchant_chat_view, name='merchant_chat'),
    path('merchant/chat/send/', chat_views.merchant_send_message, name='merchant_send_message'),
    path('merchant/transactions/', chat_views.merchant_transactions_view, name='merchant_transactions'),
    
    # Chat API
    path('api/chat/get_new_messages/', chat_views.get_new_messages, name='get_new_messages'),
    
    # Default redirect
    path('', lambda request: redirect('/login/')),
]