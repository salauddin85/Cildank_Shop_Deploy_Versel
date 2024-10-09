from django.urls import path, include
from .views import PurchaseProductView
from rest_framework.routers import DefaultRouter
 
from .views import  PurchaseCartView,PurchaseProductallView

router = DefaultRouter()
router.register('purchase_all',PurchaseProductallView, basename='purchase')
urlpatterns = [
    path('', include(router.urls)),
    path("list/<int:id>",PurchaseProductView.as_view(),name='purchase'),
    path("payment_cart/",PurchaseCartView.as_view(),name='purchase'),

] 