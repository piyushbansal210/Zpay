from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('easebuzz/', include('easebuzz.urls')),
    path('', include('dashboard.urls')),
]
