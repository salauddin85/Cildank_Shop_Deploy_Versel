from rest_framework import serializers
from .models import Category,Sub_Category


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Sub_Category
        fields = '__all__'
        