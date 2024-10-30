# # serializers.py
# from rest_framework import serializers
from .models import PurchaseModel
# serializers.py
from rest_framework import serializers
from .models import Payment
from cloth_product.serializers import ProductSerializer


class PurchaseSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseModel
        fields = ['']
        # fields = ['product']
   




class PurchaseProductSerialaizer(serializers.ModelSerializer):
    product = ProductSerializer( read_only=True)

    class Meta:
        model = PurchaseModel
        fields =['id', 'user', 'product']






class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'transaction_id', 'status', 'created_at']
