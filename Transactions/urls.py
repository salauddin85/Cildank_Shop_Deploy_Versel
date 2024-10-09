from django.urls import path, include
from .views import DepositView

from rest_framework.routers import DefaultRouter
from .views import DepositView
 

router = DefaultRouter()
# router.register('deposit',DepositView)
urlpatterns = [
    path('deposit/',DepositView.as_view(),name='deposit'),
    # path('', include(router.urls)),

]
 