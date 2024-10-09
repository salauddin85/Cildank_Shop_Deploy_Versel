from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CategoryApiView,SubCategoryApiView
router = DefaultRouter()

router.register('category_list',CategoryApiView, basename='category')
router.register('subcategory_list',SubCategoryApiView, basename='sub_category')

urlpatterns = [
    path('', include(router.urls)),
    # path('list/', CategoryApiView.as_view(), name='category-list'),

]