# Add this to dashboard/views_auth.py (or create new file dashboard/unified_auth.py)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User


def unified_login_view(request):
    """
    Unified login for both Admin and Merchant
    Automatically redirects based on user role
    """
    # If already logged in, redirect based on role
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/dashboard/home/')
        else:
            return redirect('/merchant/chat/')
    
    if request.method == "POST":
        username_or_email = request.POST.get("username")
        password = request.POST.get("password")
        
        # Try to authenticate with username first
        user = authenticate(request, username=username_or_email, password=password)
        
        # If that fails, try to find user by email and authenticate
        if user is None:
            try:
                # Look up user by email
                user_obj = User.objects.get(email=username_or_email)
                # Authenticate with the username
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        
        if user is not None:
            # Check if merchant account exists and is active (for non-staff users)
            if not user.is_staff:
                try:
                    from easebuzz.models import Merchant
                    merchant = user.merchant
                    if not merchant.is_active:
                        messages.error(request, "Your merchant account is inactive. Please contact admin.")
                        return render(request, "auth/unified_login.html")
                except:
                    messages.error(request, "Merchant profile not found. Please contact admin.")
                    return render(request, "auth/unified_login.html")
            
            # Login successful - redirect based on role
            login(request, user)
            
            if user.is_staff:
                # Redirect admin to dashboard
                return redirect('/dashboard/home/')
            else:
                # Redirect merchant to chat
                return redirect('/merchant/chat/')
        else:
            messages.error(request, "Invalid username/email or password.")
    
    return render(request, "auth/unified_login.html")


def unified_logout_view(request):
    """Unified logout for both Admin and Merchant"""
    logout(request)
    return redirect('/login/')