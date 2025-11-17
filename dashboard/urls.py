from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.home, login_url='/auth/login/'), name='dashboard_home'),
    path('home/', login_required(views.home, login_url='/auth/login/'), name='dashboard_home'),
    path('easebuzz/', views.easebuzz_dashboard, name='easebuzz_dashboard'),


]
