from django.shortcuts import render
from rest_framework import viewsets
from .models import Product,Wishlist,Review
from .serializers import WishlistSerializer,ReviewSerializer,ProductSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework import status,pagination
from .constraints import SIZE
from cloth_category.models import Category,Sub_Category
from rest_framework.views import APIView
from auth_app.models import Account
from django.http import Http404


class ProductPagination(pagination.PageNumberPagination):
    page_size = 12 # items per page
    page_size_query_param = page_size
    max_page_size = 100

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class=ProductPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

   
    
    @action(detail=False, methods=['get'],url_path='sorted_by_size/(?P<size>[^/.]+)')
    def sorted_by_size(self, request,size):
        
        if any(size == s[0] for s in SIZE):
            print("Size in SIZE")
            
            products = Product.objects.filter(size=size)
        else:
            products = Product.objects.all()
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
       
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    @action(detail=False, methods=['get'], url_path='sorted_by_category/(?P<category>[^/.]+)')
    def sorted_by_category(self, request, category):
        try:
            products = Product.objects.filter(sub_category__category__name=category)
            
            if not products.exists():
                return Response({'error': "No Product found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Product.DoesNotExist:
            return Response({'error': "No Product found"}, status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
       
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='sorted_by_sub_category/(?P<category>[^/.]+)')
    def sorted_by_sub_category(self, request, category):
        try:
            products = Product.objects.filter(sub_category__name=category)
            
            if not products.exists():
                return Response({'error': "No Product found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Product.DoesNotExist:
            return Response({'error': "No Product found"}, status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
       
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    @action(detail=False, methods=['get'], url_path='sorted_by_color/(?P<color>[^/.]+)')
    def sorted_by_color(self, request, color):
        try:
            products = Product.objects.filter(color=color)
            
            if not products.exists():
                return Response({'error': "No Product found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Product.DoesNotExist:
            return Response({'error': "No Product found"}, status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
       
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'], url_path='sorted_by_search/(?P<search>[^/.]+)')
    def sorted_by_search(self, request, search):
        try:
            # Filter products by name starting with the search term or containing it
            products = Product.objects.filter(name__icontains=search)
            
            if not products.exists():
                return Response({'error': "No Product found"}, status=status.HTTP_404_NOT_FOUND)

        except Product.DoesNotExist:
            return Response({'error': "No Product found"}, status=status.HTTP_404_NOT_FOUND)

        # Paginate the results if pagination is required
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Serialize and return the products
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    






    @action(detail=False, methods=['get'])
    def sorted_by_price(self, request):
        sort_order = request.query_params.get('order', 'asc')
        if sort_order == 'asc':
            products = Product.objects.all().order_by('price')
        elif sort_order == 'desc':
            products = Product.objects.all().order_by('-price')
        else:
            products = Product.objects.all()

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    





class WishlistViewset(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Wishlist.objects.filter(user=user)
        return Wishlist.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not Wishlist.objects.filter(user=user).exists():
            serializer.save(user=user)

    @action(detail=False, methods=['post'], url_path=r'add_product/(?P<product_id>\d+)')
    def add_product(self, request, product_id=None):
        user = request.user
        wishlist, created = Wishlist.objects.get_or_create(user=user)
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if product.quantity>0:
            if product in wishlist.products.all():
                return Response({'status': 'Product already in wishlist.'}, status=status.HTTP_200_OK)
            
            wishlist.products.add(product)
            return Response({'status': 'Product added to wishlist.'}, status=status.HTTP_200_OK)
        else:
            return Response("Product quantity not available")
    @action(detail=False, methods=['post'], url_path=r'remove_product/(?P<product_id>\d+)')
    def remove_product(self, request, product_id=None):
        user = request.user
        try:
            wishlist = Wishlist.objects.get(user=user)
            product = Product.objects.get(id=product_id)
        except Wishlist.DoesNotExist:
            return Response({'error': 'Wishlist does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        if product not in wishlist.products.all():
            return Response({'status': 'Product not found in wishlist.'}, status=status.HTTP_200_OK)
        
        wishlist.products.remove(product)
        return Response({'status': 'Product removed from wishlist.'}, status=status.HTTP_200_OK)
    


from rest_framework.parsers import MultiPartParser, FormParser


class ReviewViewset(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    parser_classes = [MultiPartParser, FormParser]  # ফাইল ও ফর্ম ডাটা হ্যান্ডেল করার জন্য

    @action(detail=False, methods=['post'], url_path='add_review')
    def add_review(self, request, id):
        # Get the product instance
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response("Product does not exist.", status=status.HTTP_404_NOT_FOUND)

        # Check if a review already exists for this product by the current user
        review_exists = Review.objects.filter(products=product, reviewer=request.user).exists()
        if review_exists:
            return Response("This product review already exists.", status=status.HTTP_400_BAD_REQUEST)

        # Get the account of the user
        try:
            account = Account.objects.get(user=request.user)
            name = f"{account.user.first_name} {account.user.last_name}"

            # Create the review instance with all fields
            review_data = {
                'products': product.id,  # Single product ID for ForeignKey
                'name': name,
                'rating': request.data.get('rating'),
                'image': request.FILES.get('image', None),  # Image ফাইলটি request.FILES থেকে নেবে
                'body': request.data.get('body', '')
            }

            # Create and validate the serializer
            serializer = self.get_serializer(data=review_data)
            serializer.is_valid(raise_exception=True)

            # Save the review using perform_create with additional fields
            self.perform_create(serializer, name=name, products=product)

            return Response("Review added successfully.", status=status.HTTP_201_CREATED)
        except Account.DoesNotExist:
            return Response("Unknown Account Holder", status=status.HTTP_404_NOT_FOUND)
    
    # Perform Create function override
    def perform_create(self, serializer, name, products):
        serializer.save(reviewer=self.request.user, name=name, products=products)