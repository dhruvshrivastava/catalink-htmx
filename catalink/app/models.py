from django.db import models
from django.contrib.auth.models import User

class Catalog(models.Model):
    name = models.CharField(max_length=250)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(default="", null=False, unique=True)

    def __str__(self):
        return self.name 

class Product(models.Model):
    product_name = models.CharField(max_length=250)
    product_description = models.CharField(max_length=1000)
    product_price = models.IntegerField(max_length=100)
    under_catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name 
    


