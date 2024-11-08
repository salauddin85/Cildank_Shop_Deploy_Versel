from rest_framework import serializers
from .models import Product,Wishlist,Review
from django.contrib.auth.models import User
from .constraints import STAR_CHOICES,SIZE

from rest_framework import serializers
from .models import Product,CoustomerWishlistProduct
from .models import Sub_Category

class ProductSerializer(serializers.ModelSerializer):
    # Admin এর জন্য PrimaryKeyRelatedField ব্যবহার করা
    sub_category = serializers.PrimaryKeyRelatedField(queryset=Sub_Category.objects.all(), required=False)
    
    # User এর জন্য CharField ব্যবহার করা
    sub_category_name = serializers.CharField(source='sub_category.name', read_only=True)
    
    is_low_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'sub_category', 'sub_category_name', 'image', 'price', 'quantity', 'description', 'size', 'color', 'is_low_stock', 'low_stock_threshold']

    def get_is_low_stock(self, obj):
        return obj.is_low_stock()

    # perform_create এ `sub_category` সঠিকভাবে হ্যান্ডেল করা
    def perform_create(self, serializer):
        if 'sub_category' in self.context['request'].data:
            sub_category = Sub_Category.objects.get(id=self.context['request'].data['sub_category'])
            serializer.save(user=self.context['request'].user, sub_category=sub_category)
        else:
            serializer.save(user=self.context['request'].user)


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
