# serializers.py
from rest_framework import serializers
from .models import PurchaseModel

from cloth_product.serializers import ProductSerializer
class PurchaseSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseModel
        fields = ['']
        # fields = ['product']
   
# class PurchaseCartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PurchaseCartModel
#         fields = ['']


# class PurchaseCartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PurchaseCartModel
#         fields = ['']  # Serialize the user and products




class PurchaseProductSerialaizer(serializers.ModelSerializer):
    product = ProductSerializer( read_only=True)

    class Meta:
        model = PurchaseModel
        fields =['id', 'user', 'product']