from django.urls import path, include
# from .views import PurchaseProductView
from rest_framework.routers import DefaultRouter
from .views import (SSLCommerzPaymentView,
                     SSLCommerzPaymentSuccessView,
                       SSLCommerzPaymentFailView,
                       PurchaseProductallView,
                       PaymentDetailsView,OrderViewset,AdminReportView)





router = DefaultRouter()
router.register('purchase_details',PurchaseProductallView, basename='purchase')
router.register('payment_details',PaymentDetailsView, basename='paymentdetails')
# router.register('customer_order',OrderViewset, basename='order')
urlpatterns = [
    path('', include(router.urls)),
    path('payment/initiate/', SSLCommerzPaymentView.as_view(), name='payment_initiate'),
    path('payment/success/<str:tran_id>/<int:user_id>/', SSLCommerzPaymentSuccessView.as_view(), name='payment_success'),
    path('payment/fail/<str:tran_id>/<int:user_id>/', SSLCommerzPaymentFailView.as_view(), name='payment_fail'),
    path('AdminReportView/', AdminReportView.as_view(), name='AdminReport'),
    path('order/', OrderViewset.as_view(), name='order-list'),  # GET and POST for listing and creating orders
    path('order/<int:order_id>/', OrderViewset.as_view(), name='order-detail'),  # GET, PUT, PATCH, DELETE for a specific order
]
