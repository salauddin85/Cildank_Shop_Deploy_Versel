from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    account_no = models.IntegerField(unique=True,auto_created=True) 
    balance = models.DecimalField(decimal_places=2,max_digits=10,default=0)   
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f"{self.user.first_name} {self.user.last_name}  {self.account_no} "
    
class ContactUs(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message=models.TextField(max_length=500)

    def __str__(self) :
        return f"Name : {self.name} Email : {self.email} "