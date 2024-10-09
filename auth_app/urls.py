from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .import views
from  .views import  UserRegistrationApiView,UserLoginApiView,activate,UserLogoutView,AccountView,ContactUsView
router = DefaultRouter() # amader router
router.register('account',AccountView, basename='account')
router.register('contactus',ContactUsView, basename='contactus')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationApiView.as_view(), name='register'),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
   
]