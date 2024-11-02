from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Product,Wishlist,Review,CoustomerWishlistProduct
from .serializers import WishlistSerializer,ReviewSerializer,ProductSerializer,WishlistProductSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework import status,pagination
from .constraints import SIZE
from cloth_category.models import Category,Sub_Category
from rest_framework.views import APIView
from auth_app.models import Account
from django.http import Http404
from django.contrib.auth.models import User
# from rest_framework.parsers import MultiPartParser, FormParser
import cloudinary.uploader
from auth_app.permissions import IsAdmin,IsCustomer
from django.db.models import F


class ProductPagination(pagination.PageNumberPagination):
    page_size = 12 # items per page
    page_size_query_param = page_size
    max_page_size = 100

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class=ProductPagination


    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return [permissions.IsAuthenticatedOrReadOnly()]
        else:
            return [IsAdmin()]  # Custom permission for admin actions

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

#    Low stock products endpoint
    @action(detail=False, methods=['get'], url_path='low_stock')
    def low_stock_products(self, request):
        low_stock_products = Product.objects.filter(quantity__lte=F('low_stock_threshold'))
        page = self.paginate_queryset(low_stock_products)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(low_stock_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
            return Wishlist.objects.filter(user=user).prefetch_related('wishlist_products')
        return Wishlist.objects.none()


    def perform_create(self, serializer):
        user = self.request.user
        if not Wishlist.objects.filter(user=user).exists():
            serializer.save(user=user)

    @action(detail=False, methods=['post'], url_path=r'add_product/(?P<product_id>\d+)/(?P<quantity>\d+)')
    def add_product(self, request, product_id=None, quantity=1):
        user = request.user
        quantity=int(quantity)
        # Wishlist তৈরি বা খুঁজে বের করা
        wishlist, created = Wishlist.objects.get_or_create(user=user)

        try:
            # Product পাওয়ার চেষ্টা
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # উইশলিস্টে পণ্যটি আগে থেকেই আছে কিনা পরীক্ষা করা
        wishlist_product, created = CoustomerWishlistProduct.objects.get_or_create(wishlist=wishlist, product=product)

        if not created:  # যদি আগে থেকেই থাকে
            wishlist_product.quantity += quantity  # পরিমাণ বাড়ান
            wishlist_product.save()
            return Response({"status": "Product quantity updated in wishlist."}, status=status.HTTP_200_OK)
        
        # নতুন পণ্য যোগ করুন
        wishlist_product.quantity = quantity
        wishlist_product.save()
        return Response({'status': 'Product added to wishlist successfully.'}, status=status.HTTP_200_OK)



        
    @action(detail=False, methods=['post'], url_path=r'remove_product/(?P<product_id>\d+)')
    def remove_product(self, request, product_id=None):
        user = request.user
        try:
            # User এর Wishlist এবং Product খুঁজে পাওয়া
            wishlist = Wishlist.objects.get(user=user)
            wishlist_product = CoustomerWishlistProduct.objects.get(wishlist=wishlist, product_id=product_id)
        except Wishlist.DoesNotExist:
            return Response({'error': 'Wishlist does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        except CoustomerWishlistProduct.DoesNotExist:
            return Response({'error': 'Product not found in wishlist.'}, status=status.HTTP_404_NOT_FOUND)

        # উইশলিস্ট থেকে পণ্যটি সরিয়ে ফেলা
        wishlist_product.delete()
        return Response({'status': 'Product removed from wishlist.'}, status=status.HTTP_200_OK)



class ReviewViewset(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly,IsAdmin]
    lookup_field = 'id'

    

    def get_queryset(self):
        # if admin show all review otherwise just reqeust.user see his/her review
        if self.request.user.is_staff:
            return Review.objects.all()
        return Review.objects.filter(reviewer=self.request.user)
    
    @action(detail=False, methods=['get'], url_path='reviews_by_product')
    def reviews_by_product(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product does not exist."}, status=status.HTTP_404_NOT_FOUND)

        reviews = Review.objects.filter(products=product)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




    @action(detail=False, methods=['post'], url_path='add_review')
    def add_review(self, request, id):
        # Get the product instance
        print("id",id)
        try:
            product = Product.objects.get(id=id)
            print(product)
        except Product.DoesNotExist:
            return Response({"error": "Product does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Check if a review already exists for this product by the current user
        review_exists = Review.objects.filter(products=product, reviewer=request.user).exists()
        if review_exists:
            return Response({"error": "This product review already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the account of the user
        try:
            account = Account.objects.get(user=request.user)
            print(account)
            name = f"{account.user.first_name} {account.user.last_name}"
            rating=request.data.get('rating')
            body=request.data.get('body', '') 
            # Retrieve image URL from request
            image_url = request.data.get("image")
            print(image_url,rating,body)
            if not image_url:
                return Response({"error": "image_url not found"}, status=status.HTTP_400_BAD_REQUEST)

            # Create the review instance with all fields
            review_data = {
                'products': product.id,
                'name': name,
                'rating':rating ,
                'image': image_url,  # Image URL
                'body':body  # Default to empty string if not provided
            }

            # Create and validate the serializer
            serializer = self.get_serializer(data=review_data)
            serializer.is_valid(raise_exception=True)

            # Save the review
            self.perform_create(serializer, name=name, products=product)

            return Response({"success": "Review added successfully."}, status=status.HTTP_201_CREATED)
        except Account.DoesNotExist:
            return Response({"error": "Unknown Account Holder"}, status=status.HTTP_404_NOT_FOUND)

    # Perform Create function override
    def perform_create(self, serializer, name, products):
        serializer.save(reviewer=self.request.user, name=name, products=products)

    @action(detail=True, methods=['delete'], permission_classes=[IsAdmin], url_path='delete_review')
    def delete_review(self, request, id=None):
        try:
            review = Review.objects.get(id=id)
            review.delete()
            return Response({"success": "Review deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response({"error": "Review not found."}, status=status.HTTP_404_NOT_FOUND)