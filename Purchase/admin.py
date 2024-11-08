from django.contrib import admin

# Register your models here.
from .models import PurchaseModel,CustomerOrder,Payment
admin.site.register(PurchaseModel)
admin.site.register(CustomerOrder)
admin.site.register(Payment)