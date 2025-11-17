from django.urls import path
from .views_auth import login_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/auth/login/'), name='logout'),
]
