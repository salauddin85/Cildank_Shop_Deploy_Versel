from django.db import models
from django.contrib.auth.models import User
from cloth_category.models import Category,Sub_Category
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .constraints import SIZE,STAR_CHOICES
from cloudinary.models import CloudinaryField
class Product(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_Category,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    image = CloudinaryField('Product_images')
    price = models.DecimalField(decimal_places=2,max_digits=10)
    quantity = models.IntegerField()
    description = models.TextField()
    size = models.CharField(max_length=100,null=True,blank=True,choices=SIZE)
    
    

    
    def __str__(self) -> str:
        return f" Product : {self.name} , Category: {self.sub_category.name}"

class Wishlist(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
   
    def __str__(self) -> str:
        return f"{self.user.first_name}{self.user.last_name} "




class Review(models.Model):
    reviewer = models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    body = models.TextField()
    name = models.CharField(max_length=50)
    image = CloudinaryField('Product_images')
    created = models.DateTimeField(auto_now_add = True)
    rating = models.CharField(choices = STAR_CHOICES, max_length = 10)
    
    def __str__(self):
        return f"Reviewer: {self.reviewer.first_name} {self.reviewer.last_name} "





