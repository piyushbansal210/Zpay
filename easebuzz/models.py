from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Merchant(models.Model):
    # User relationship for authentication
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Business Information
    merchant_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=100, blank=True, null=True)
    
    # Contact Information
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    # Tax Information
    pan = models.CharField(max_length=10, blank=True, null=True)
    gstin = models.CharField(max_length=15, blank=True, null=True)
    
    # Address Information
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    
    # Bank Information
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_no = models.CharField(max_length=50, blank=True, null=True)
    ifsc_code = models.CharField(max_length=11, blank=True, null=True)
    account_holder_name = models.CharField(max_length=255, blank=True, null=True)
    
    # Balance Information
    inr_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hold_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Status
    prepaid_status = models.CharField(
        max_length=20,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Inactive"
    )
    is_active = models.BooleanField(default=True)
    
    # Provider information
    provider = models.CharField(max_length=100, default="easebuzz")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.merchant_name
    
    @property
    def unread_messages_count(self):
        """Count unread messages from admin to this merchant"""
        return self.received_messages.filter(is_read=False, sender__is_staff=True).count()


class ChatMessage(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='chat_messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    
    message = models.TextField()
    
    is_read = models.BooleanField(default=False)
    is_from_admin = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        sender_type = "Admin" if self.is_from_admin else "Merchant"
        return f"{sender_type} message to {self.merchant.merchant_name} at {self.created_at}"
    
    def mark_as_read(self):
        if not self.is_read:
            from django.utils import timezone
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


@receiver(post_save, sender=Merchant)
def create_merchant_user(sender, instance, created, **kwargs):
    """Auto-create a user account when a merchant is created"""
    if created and not instance.user:
        # Generate username from email
        username = instance.email.split('@')[0] + str(instance.id)
        
        # Create user account
        user = User.objects.create_user(
            username=username,
            email=instance.email,
            password='merchant@123',  # Default password
            first_name=instance.merchant_name.split()[0] if instance.merchant_name else '',
        )
        user.is_staff = False
        user.is_active = True
        user.save()
        
        # Link user to merchant
        instance.user = user
        instance.save()