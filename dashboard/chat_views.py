from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Count, Max
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
import json

from easebuzz.models import Merchant, ChatMessage


# ==================== ADMIN CHAT VIEWS ====================

@login_required(login_url='/auth/login/')
def admin_chat_list(request):
    """Admin view: List all merchants with their last message"""
    if not request.user.is_staff:
        return redirect('/merchant/chat/')
    
    # Get all merchants with their last message
    merchants = Merchant.objects.filter(
        is_active=True
    ).annotate(
        unread_count=Count('chat_messages', filter=Q(chat_messages__is_read=False, chat_messages__is_from_admin=False)),
        last_message_time=Max('chat_messages__created_at')
    ).order_by('-last_message_time', '-created_at')
    
    # Get last message for each merchant
    for merchant in merchants:
        last_msg = merchant.chat_messages.last()
        merchant.last_message = last_msg.message[:50] + '...' if last_msg and len(last_msg.message) > 50 else (last_msg.message if last_msg else 'No messages yet')
        merchant.last_message_time_display = last_msg.created_at if last_msg else merchant.created_at
    
    context = {
        'merchants': merchants,
        'active_merchant_id': request.GET.get('merchant_id'),
    }
    
    return render(request, 'dashboard/pages/admin_chat.html', context)


@login_required(login_url='/auth/login/')
def admin_chat_conversation(request, merchant_id):
    """Admin view: View conversation with a specific merchant"""
    if not request.user.is_staff:
        return redirect('/merchant/chat/')
    
    merchant = get_object_or_404(Merchant, id=merchant_id)
    
    # Get all messages for this merchant
    messages_list = ChatMessage.objects.filter(merchant=merchant).select_related('sender')
    
    # Mark merchant's messages as read
    merchant_messages = messages_list.filter(is_from_admin=False, is_read=False)
    for msg in merchant_messages:
        msg.mark_as_read()
    
    context = {
        'merchant': merchant,
        'messages': messages_list,
    }
    
    return render(request, 'dashboard/partials/chat_conversation.html', context)


@login_required(login_url='/auth/login/')
@require_http_methods(["POST"])
def admin_send_message(request):
    """API: Admin sends message to merchant"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        data = json.loads(request.body)
        merchant_id = data.get('merchant_id')
        message_text = data.get('message', '').strip()
        
        if not message_text:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        merchant = get_object_or_404(Merchant, id=merchant_id)
        
        # Create message
        chat_message = ChatMessage.objects.create(
            merchant=merchant,
            sender=request.user,
            receiver=merchant.user,
            message=message_text,
            is_from_admin=True,
            is_read=False
        )
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': chat_message.id,
                'text': chat_message.message,
                'sender': request.user.get_full_name() or request.user.username,
                'created_at': chat_message.created_at.strftime('%I:%M %p'),
                'is_from_admin': True
            }
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ==================== MERCHANT CHAT VIEWS ====================

@login_required(login_url='/merchant/login/')
def merchant_chat_view(request):
    """Merchant view: Chat with admin"""
    if request.user.is_staff:
        return redirect('/dashboard/chat/')
    
    try:
        merchant = Merchant.objects.get(user=request.user)
    except Merchant.DoesNotExist:
        return render(request, 'merchant/error.html', {
            'error': 'Merchant profile not found. Please contact admin.'
        })
    
    # Get all messages for this merchant
    messages_list = ChatMessage.objects.filter(merchant=merchant).select_related('sender')
    
    # Mark admin messages as read
    admin_messages = messages_list.filter(is_from_admin=True, is_read=False)
    for msg in admin_messages:
        msg.mark_as_read()
    
    context = {
        'merchant': merchant,
        'messages': messages_list,
        'unread_count': 0  # Already marked as read
    }
    
    return render(request, 'merchant/chat.html', context)


@login_required(login_url='/merchant/login/')
@require_http_methods(["POST"])
def merchant_send_message(request):
    """API: Merchant sends message to admin"""
    if request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        merchant = Merchant.objects.get(user=request.user)
        
        data = json.loads(request.body)
        message_text = data.get('message', '').strip()
        
        if not message_text:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Create message (receiver will be any admin, or we can set to None)
        chat_message = ChatMessage.objects.create(
            merchant=merchant,
            sender=request.user,
            receiver=None,  # Any admin can see
            message=message_text,
            is_from_admin=False,
            is_read=False
        )
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': chat_message.id,
                'text': chat_message.message,
                'sender': merchant.merchant_name,
                'created_at': chat_message.created_at.strftime('%I:%M %p'),
                'is_from_admin': False
            }
        })
        
    except Merchant.DoesNotExist:
        return JsonResponse({'error': 'Merchant profile not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# ==================== MERCHANT AUTH VIEWS ====================

def merchant_login_view(request):
    """
    Merchant login page - allows login with username or email
    """
    if request.user.is_authenticated and not request.user.is_staff:
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
        
        if user is not None and not user.is_staff:
            # Check if merchant account exists
            try:
                merchant = user.merchant
                if not merchant.is_active:
                    messages.error(request, "Your merchant account is inactive. Please contact admin.")
                    return render(request, "merchant/login.html")
            except:
                messages.error(request, "Merchant profile not found. Please contact admin.")
                return render(request, "merchant/login.html")
            
            login(request, user)
            return redirect('/merchant/chat/')
        else:
            messages.error(request, "Invalid credentials or you don't have merchant access.")
    
    return render(request, "merchant/login.html")


def merchant_logout_view(request):
    """Merchant logout"""
    logout(request)
    return redirect('/merchant/login/')


@login_required(login_url='/merchant/login/')
def merchant_dashboard(request):
    """Merchant dashboard - redirect to chat for now"""
    if request.user.is_staff:
        return redirect('/dashboard/')
    
    return redirect('/merchant/chat/')