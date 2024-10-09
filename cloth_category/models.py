from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()


    def __str__(self) -> str:
        return self.name
    
class Sub_Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self) -> str:
        return self.name
    