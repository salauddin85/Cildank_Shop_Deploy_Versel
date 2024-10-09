from django.contrib import admin

# Register your models here.
from .models import TransactionsModel
admin.site.register(TransactionsModel)