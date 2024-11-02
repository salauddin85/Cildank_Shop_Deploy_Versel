from rest_framework import serializers
from .models import Product,Wishlist,Review
from django.contrib.auth.models import User
from .constraints import STAR_CHOICES,SIZE

from rest_framework import serializers
from .models import Product,CoustomerWishlistProduct


class ProductSerializer(serializers.ModelSerializer):
    sub_category = serializers.CharField(source='sub_category.name')
    is_low_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'sub_category', 'image', 'price', 'quantity', 'description', 'size', 'color', 'is_low_stock']

    def get_is_low_stock(self, obj):
        return obj.is_low_stock()


class WishlistProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = CoustomerWishlistProduct
        fields = ['product', 'quantity']

class WishlistSerializer(serializers.ModelSerializer):
    products = WishlistProductSerializer(source='wishlist_products', many=True, read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'products']


class ReviewSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'products', 'body', 'name', 'image', 'created', 'rating']
        read_only_fields = ['reviewer', 'created','name','id','products']  # 'reviewer' and 'created' are read-only
