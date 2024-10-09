
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from .constriants import TRANSACTION_TYPE

# Create your models here.
class TransactionsModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    transaction_amount = models.DecimalField(decimal_places=2,max_digits=10)
    transaction_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    transaction_type = models.CharField(max_length=50,choices=TRANSACTION_TYPE,null=True,blank=True)
    balance = models.DecimalField(decimal_places=2,max_digits=10,null=True,blank=True)
    
    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name} {self.transaction_type}"