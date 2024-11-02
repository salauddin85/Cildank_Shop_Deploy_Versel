from django.db import models
from django.contrib.auth.models import User 
from auth_app.models import Account
from cloth_product.models import Product
from Transactions.constriants import TRANSACTION_TYPE
# Create your models here.



class PurchaseModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default="Processing")
    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name} product id: {self.product.pk}'
    
# models.py



class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"

ORDER=(
    ('Processing','Processing'),
    ("Completed","Completed"),
    ("Canceled","Canceled"),
)

class CustomerOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=50,choices=ORDER, default="Processing")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.status}"
