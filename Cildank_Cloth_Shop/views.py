
# from rest_framework import viewsets
# from cloth_product.models import Product
# from cloth_product.serialaizers import ProductSerializer
# from cloth_category.serializers import CategorySerializer,SubCategorySerializer
# from cloth_category.models import Category,Sub_Category
# # class ShowAllProductViewset(viewsets.ModelViewSet):

# #     queryset = Product.objects.all()
# #     serializer_class = ProductSerializer

# #     def get_queryset(self): 
# #         queryset = super().get_queryset()
# #         print(queryset)
# #         user_slug = self.request.query_params.get('category_id')
# #         print("user_slug",user_slug)
# #         if user_slug:
# #             queryset = queryset.filter(category_id = user_slug)
# #             print("after user slug",queryset)
            
# #         return  queryset

# class ShowAllProductViewset(viewsets.ModelViewSet):

#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#     def get_queryset(self): 
#         queryset = super().get_queryset()
#         print(queryset)
#         category_id = self.request.query_params.get('category_id')
#         subcategory_id = self.request.query_params.get('sub_category_id')
#         print("category_slug",category_id)
#         print("sub_category_slug",subcategory_id)

#         if subcategory_id:
#             queryset = queryset.filter(sub_category_id=subcategory_id)

#         elif category_id:
#             # Filter products based on the category
#             queryset = queryset.filter(sub_category__category_id=category_id)
            
#         return  queryset
