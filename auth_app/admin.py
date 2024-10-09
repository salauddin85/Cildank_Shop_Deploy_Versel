from django.contrib import admin
from .models import Account,ContactUs
from django.contrib.auth.models import User
# # # Register your models here.
# 'first_name', 'last_name', 'email', 

class AccountAdmin(admin.ModelAdmin):
    list_display = ['account_no', 'balance', 'created_on']

    # def first_name(self, obj):
    #     return obj.user.first_name

    # def last_name(self, obj):
    #     return obj.user.last_name

    # def email(self, obj):
    #     return obj.user.email

            
admin.site.register(Account, AccountAdmin)
admin.site.register(ContactUs)