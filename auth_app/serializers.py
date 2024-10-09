from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.permissions import BasePermission
# permission_class = [IsAuthenticated] or [IsAuthenticatedOrReadOnly] use korte pari 

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account,ContactUs

class UserRegistrationSerialaizer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'password', 'email', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        email = data['email']
        if data['password'] != data['confirm_password']:

            raise serializers.ValidationError("Passwords does not match")
        
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error' : "Email Already exists"})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name')
        )
        user.is_active=False
        user.save()
        Account.objects.create(
                user = user,
                account_no = 100000+user.id
            )
        return user
    




# class RegistrationSerializer(serializers.ModelSerializer):
#     confirm_password = serializers.CharField(required = True)
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
    
#     def save(self):
#         username = self.validated_data['username']
#         first_name = self.validated_data['first_name']
#         last_name = self.validated_data['last_name']
#         email = self.validated_data['email']
#         password = self.validated_data['password']
#         password2 = self.validated_data['confirm_password']
        
#         if password != password2:
#             raise serializers.ValidationError({'error' : "Password Doesn't Mactched"})
#         if User.objects.filter(email=email).exists():
#             raise serializers.ValidationError({'error' : "Email Already exists"})
#         user = User(username = username, email=email, first_name = first_name, last_name = last_name)
#         print(user)
#         user.set_password(password)
#         user.is_active = False
#         user.save()
#         Account.objects.create(
#                 user = user,
#                 account_no = 100000+user.id
#             )
#         return user
















class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)





class AccountSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    class Meta:
        model = Account
        fields = ['user_name', 'account_no', 'balance', 'created_on']

       





class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"


