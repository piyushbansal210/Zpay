from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('easebuzz/', include('easebuzz.urls')),
    path('razorpay/', include('razorpay.urls')),
    path('payu/', include('payu.urls')),
    path('stripe/', include('stripe.urls')),
]
