# dashboard/auth_urls.py - FIXED VERSION

from django.urls import path
from .views_auth import unified_login_view, unified_logout_view

urlpatterns = [
    # Use unified login/logout
    path('login/', unified_login_view, name='admin_login'),
    path('logout/', unified_logout_view, name='admin_logout'),
]