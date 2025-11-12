from django.db import models

class Merchant(models.Model):
    business_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    inr_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    hold_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    prepaid_status = models.CharField(
        max_length=20,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Inactive"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.business_name
