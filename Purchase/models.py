from django.db import models
from django.contrib.auth.models import User 
from auth_app.models import Account
from cloth_product.models import Product
from Transactions.constriants import TRANSACTION_TYPE
# Create your models here.



class PurchaseModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)


    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name} product id: {self.product.pk}'
    

# class PurchaseCartModel(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE)
   


# class PurchaseCartModel(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
#     product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    
#     def __str__(self) -> str:
#         return f'{self.user.first_name} {self.user.last_name} product id: {self.product.pk}'
    
