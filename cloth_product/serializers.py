from rest_framework import serializers
from .models import Product,Wishlist,Review
from django.contrib.auth.models import User
from .constraints import STAR_CHOICES,SIZE

from rest_framework import serializers
from .models import Product




class ProductSerializer(serializers.ModelSerializer):
    sub_category = serializers.CharField(source='sub_category.name')

    # size = serializers.MultipleChoiceField(choices = SIZE)
    # size = serializers.ListField(child=serializers.ChoiceField(choices=SIZE))

    class Meta:
        
        model = Product
        # fields = '__all__'

        fields = ['id','name','sub_category','image','price','quantity','description','size','color']




class WishlistSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'products']



# from rest_framework import serializers
# from .models import Review

# class ReviewSerializer(serializers.ModelSerializer):
#     products = ProductSerializer(many=False, read_only=True)
#     name = serializers.CharField(read_only=True)
#     class Meta:
#         model = Review
#         fields = ['id', 'reviewer','products','name', 'body', 'image', 'created', 'rating']
       
from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'products', 'body', 'name', 'image', 'created', 'rating']
        read_only_fields = ['reviewer', 'created','name']  # 'reviewer' and 'created' are read-only
