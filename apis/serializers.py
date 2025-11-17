from rest_framework import serializers

class AddMerchantSerializer(serializers.Serializer):
    merchant_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(required=True)
    business_type = serializers.CharField(required=True)
    pan = serializers.CharField(required=True)
    gstin = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    city = serializers.CharField(required=True)
    state = serializers.CharField(required=True)
    pincode = serializers.CharField(required=True)
    bank_name = serializers.CharField(required=True)
    account_no = serializers.CharField(required=True)
    ifsc_code = serializers.CharField(required=True)
