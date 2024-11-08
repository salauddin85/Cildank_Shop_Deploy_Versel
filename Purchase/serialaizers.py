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
    username = serializers.CharField(source='user.username', read_only=True)  # Make it read-only

    class Meta:
        model = CustomerOrder
        fields = ['id', 'user', 'username', 'product', 'quantity', 'total_price', 'status', 'created_at']
        read_only_fields = ['created_at', 'user']  # Adding user as read-only if needed

        def validate_status(self, value):
            allowed_statuses = ["Completed", "Canceled", "Processing"]
            if value not in allowed_statuses:
                raise serializers.ValidationError(f"Invalid status. Allowed statuses are: {', '.join(allowed_statuses)}")
            return value