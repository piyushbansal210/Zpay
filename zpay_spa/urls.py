from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    path('dashboard/', include('dashboard.urls')),    # protected area
    path('auth/', include('dashboard.auth_urls')),    # login/logout

    path('easebuzz/', include('easebuzz.urls')),
    path('api/', include('apis.urls')),

    # DEFAULT: If user is logged in → go to dashboard
    # If not logged in → go to login
    path('', lambda request: redirect('/dashboard/home/') if request.user.is_authenticated else redirect('/auth/login/')),
]
