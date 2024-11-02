from django.contrib import admin

# Register your models here.
from .models import PurchaseModel
admin.site.register(PurchaseModel)