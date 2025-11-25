# Add these to your dashboard/urls.py

from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from . import chat_views  # Import the new chat views

urlpatterns = [
    # Existing routes
    path('', login_required(views.home, login_url='/auth/login/'), name='dashboard_home'),
    path('home/', login_required(views.home, login_url='/auth/login/'), name='dashboard_home'),
    path('easebuzz/', views.easebuzz_dashboard, name='easebuzz_dashboard'),
    
    # Chat routes for admin
    path('chat/', chat_views.admin_chat_list, name='admin_chat_list'),
    path('chat/conversation/<int:merchant_id>/', chat_views.admin_chat_conversation, name='admin_chat_conversation'),
    path('chat/send/', chat_views.admin_send_message, name='admin_send_message'),
]