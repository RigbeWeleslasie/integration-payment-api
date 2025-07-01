from rest_framework import serializers
# from catalogue.models import Product


from .models import Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        Model=Product
        fields="__all__"

class MpesaPaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    phone_number = serializers.CharField(max_length=15)