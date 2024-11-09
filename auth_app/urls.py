from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .import views
from  .views import  UserRegistrationApiView,UserLoginApiView,activate,UserLogoutView,AccountView,ContactUsView,AdminAccountView,SuperuserViewSet,ProfileViewSet
router = DefaultRouter() # amader router
router.register(r'superusers', SuperuserViewSet, basename='superuser')

router.register('account',AccountView, basename='account')
router.register('admin-account', AdminAccountView, basename='admin-account')  # admin-specific view
router.register('contactus',ContactUsView, basename='contactus')
router.register('profile',ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationApiView.as_view(), name='register'),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
 
    # path('superusercreate/',SuperuserCreateView.as_view(),name="superusercreate")
]