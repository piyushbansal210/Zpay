from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger schema setup
schema_view = get_schema_view(
    openapi.Info(
        title="Easebuzz Aggregator API",
        default_version="v1",
        description="APIs for Merchant Onboarding, Listing, Payin & Payout via Easebuzz",
        contact=openapi.Contact(email="support@zpay.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('easebuzz/', include('easebuzz.urls')),
    path('api/', include('apis.urls')),

    # ✅ Swagger and Redoc routes
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # ✅ Default redirect to Add Merchant page
    path('', include('dashboard.urls')),

]
