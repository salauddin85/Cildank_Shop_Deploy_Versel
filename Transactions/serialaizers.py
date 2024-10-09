from rest_framework import serializers

from .models import TransactionsModel
class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionsModel
        fields = ['transaction_amount','transaction_type']

        
    