from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework import viewsets
# Create your views here.
from .serializers import CategorySerializer,SubCategorySerializer
from .models import Category,Sub_Category

from rest_framework.decorators import action
from rest_framework.response import Response

class CategoryApiView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def custom_action(self, request):
        return Response({'message': 'This is a custom action'})
    

class SubCategoryApiView(viewsets.ModelViewSet):
    queryset = Sub_Category.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def custom_action(self, request):
        return Response({'message': 'This is a custom action'})