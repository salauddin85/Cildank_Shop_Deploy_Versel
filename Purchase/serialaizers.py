# # serializers.py
# from rest_framework import serializers
from .models import PurchaseModel
# serializers.py
from rest_framework import serializers
from .models import Payment,CustomerOrder
from cloth_product.serializers import ProductSerializer
from cloth_product.models import Product

# class PurchaseSerializer(serializers.ModelSerializer):
#     # product = ProductSerializer(many=True, read_only=True)

#     class Meta:
#         model = PurchaseModel
#         fields = ['']
#         # fields = ['product']
   




class PurchaseProductSerialaizer(serializers.ModelSerializer):
    product = ProductSerializer( read_only=True)

    class Meta:
        model = PurchaseModel
        fields =['id', 'user', 'product','created_at','status']






class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'transaction_id', 'status', 'created_at']


class CustomerOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = CustomerOrder
        fields = ['id', 'user', 'product', 'quantity', 'total_price', 'status', 'created_at']
