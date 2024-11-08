from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from cloth_product.models import Wishlist  
from . import serializers
from .models import Account,ContactUs
from rest_framework import status
from .permissions import IsAdmin, IsCustomer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework.permissions import AllowAny



class UserRegistrationApiView(APIView):
    serializers_class = serializers.UserRegistrationSerialaizer

    def post(self, request):
        serializer = self.serializers_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            
            Wishlist.objects.create(user=user)
            
            token = default_token_generator.make_token(user)
            print("token", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print('Uid', uid)
            confirm_link = f"https://cildank-shop-deploy-versel.vercel.app/auth/active/{uid}/{token}/"
            email_subject = "Confirm Your Email"
            email_body = render_to_string("confirm_email.html", {"confirm_link": confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()

            return Response("Form submission Done",status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

def activate(request, token, uid64):
    print(token)
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        print(uid)
        user = User._default_manager.get(pk=uid)
        print(user)
    except(User.DoesNotExist):
        user = None
    print(user)
    if user is not None and default_token_generator.check_token(user, token):
        
        user.is_active = True
        user.save()
        return redirect('https://salauddin85.github.io/Cildank_Shop/login.html')
        # return redirect("login")


class UserLoginApiView(APIView):
    

    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                is_admin = user.is_staff or user.is_superuser
                print(f"User{user} IS admin:{is_admin}TOken:{token}")
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'is_admin': is_admin,
                    'username': user.username,  # ইউজারনেম যুক্ত করা হলো
                    'email': user.email  # ইমেইল যুক্ত করা হলো
                })
            else:
                return Response({'error': "Invalid Credentials"}, status=400)
        return Response(serializer.errors, status=400)

class UserLogoutView(APIView):
    def post(self, request):
        try:
            user = request.user
            print(user)
            token = Token.objects.get(user=user)
            print(token)
            token.delete()
            logout(request)
            return Response({"ok":True}) 
        except Token.DoesNotExist:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)



# class UserLogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         request.user.auth_token.delete()
#         logout(request)
#         return redirect('login')

class AccountView(viewsets.ModelViewSet):
    serializer_class = serializers.AccountSerializer
    permission_classes = [IsAuthenticated, IsCustomer]  # শুধুমাত্র customer দেখতে পারে

    def get_queryset(self):
        # শুধুমাত্র লগইন করা ইউজারের অ্যাকাউন্ট
        return Account.objects.filter(user=self.request.user)





class AdminAccountView(viewsets.ModelViewSet):
    serializer_class = serializers.AccountSerializer
    permission_classes = [IsAuthenticated, IsAdmin]  # শুধুমাত্র admin দেখতে পারে

    def get_queryset(self):
        # সমস্ত লগ ইন করা ইউজারদের অ্যাকাউন্ট দেখাচ্ছে
        return Account.objects.filter(user__in=User.objects.filter(is_active=True))




class ContactUsView(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = serializers.ContactUsSerializer
    permission_classes = [IsAdminUser]  # শুধুমাত্র admin মেসেজগুলো দেখবে


class SuperuserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # প্রয়োজন অনুযায়ী এটি সীমাবদ্ধ করুন
    serializer_class = serializers.SuperuserSerializer
    permission_classes=[IsAdminUser]
    
    def get_queryset(self):
        return User.objects.filter(is_staff=True)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'message': 'Superuser created successfully.'}, status=status.HTTP_201_CREATED)