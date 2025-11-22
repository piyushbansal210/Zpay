# MERCHANT LOGIN DEBUGGING & FIX SCRIPT
# Run this in Django shell: python manage.py shell

from django.contrib.auth.models import User
from easebuzz.models import Merchant

# ============================================
# STEP 1: CHECK IF MERCHANT EXISTS
# ============================================

print("\n" + "="*50)
print("CHECKING MERCHANTS IN DATABASE")
print("="*50 + "\n")

merchants = Merchant.objects.all()
print(f"Total Merchants: {merchants.count()}\n")

for merchant in merchants:
    print(f"Merchant ID: {merchant.id}")
    print(f"Name: {merchant.merchant_name}")
    print(f"Email: {merchant.email}")
    print(f"Has User Account: {'YES' if merchant.user else 'NO'}")
    if merchant.user:
        print(f"  → Username: {merchant.user.username}")
        print(f"  → User ID: {merchant.user.id}")
        print(f"  → Is Staff: {merchant.user.is_staff}")
        print(f"  → Is Active: {merchant.user.is_active}")
    print("-" * 40)

# ============================================
# STEP 2: CREATE TEST MERCHANT (if needed)
# ============================================

print("\n" + "="*50)
print("CREATING TEST MERCHANT")
print("="*50 + "\n")

# Check if test merchant exists
test_email = "test@merchant.com"

try:
    test_merchant = Merchant.objects.get(email=test_email)
    print(f"✓ Test merchant already exists: {test_merchant.merchant_name}")
except Merchant.DoesNotExist:
    # Create test merchant
    test_merchant = Merchant.objects.create(
        merchant_name="Test Merchant Store",
        business_type="E-commerce",
        email=test_email,
        phone="9876543210",
        pan="ABCDE1234F",
        address="123 Test Street",
        city="Mumbai",
        state="Maharashtra",
        pincode="400001",
        is_active=True,
        prepaid_status="Active"
    )
    print(f"✓ Created new merchant: {test_merchant.merchant_name}")

# ============================================
# STEP 3: CREATE/FIX USER ACCOUNT
# ============================================

print("\n" + "="*50)
print("CREATING/FIXING USER ACCOUNT")
print("="*50 + "\n")

# Check if merchant has user
if not test_merchant.user:
    # Generate username
    username = test_email.split('@')[0]  # "test"
    
    # Check if username exists, add number if needed
    if User.objects.filter(username=username).exists():
        username = f"{username}{test_merchant.id}"
    
    # Create user
    user = User.objects.create_user(
        username=username,
        email=test_email,
        password='Test123456',  # SET YOUR PASSWORD HERE
        first_name='Test',
    )
    user.is_staff = False
    user.is_active = True
    user.save()
    
    # Link to merchant
    test_merchant.user = user
    test_merchant.save()
    
    print(f"✓ Created user account")
    print(f"  Username: {username}")
    print(f"  Email: {test_email}")
    print(f"  Password: Test123456")
else:
    # User exists, just update password
    user = test_merchant.user
    user.set_password('Test123456')  # SET YOUR PASSWORD HERE
    user.save()
    
    print(f"✓ Updated existing user password")
    print(f"  Username: {user.username}")
    print(f"  Email: {user.email}")
    print(f"  Password: Test123456")

# ============================================
# STEP 4: VERIFY LOGIN CREDENTIALS
# ============================================

print("\n" + "="*50)
print("LOGIN CREDENTIALS")
print("="*50 + "\n")

print("🔑 Use these credentials to login:")
print(f"  URL: http://127.0.0.1:8000/merchant/login/")
print(f"  Email: {test_email}")
print(f"  OR Username: {user.username}")
print(f"  Password: Test123456")
print()

# ============================================
# STEP 5: TEST AUTHENTICATION
# ============================================

print("\n" + "="*50)
print("TESTING AUTHENTICATION")
print("="*50 + "\n")

from django.contrib.auth import authenticate

# Test with username
test_user = authenticate(username=user.username, password='Test123456')
if test_user:
    print(f"✓ Authentication with USERNAME works!")
else:
    print(f"✗ Authentication with username FAILED")

# Test with email
try:
    user_obj = User.objects.get(email=test_email)
    test_user = authenticate(username=user_obj.username, password='Test123456')
    if test_user:
        print(f"✓ Authentication with EMAIL works!")
    else:
        print(f"✗ Authentication with email FAILED")
except User.DoesNotExist:
    print(f"✗ User with email not found")

print("\n" + "="*50)
print("DONE!")
print("="*50 + "\n")