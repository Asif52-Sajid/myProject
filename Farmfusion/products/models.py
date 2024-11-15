from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=00)
    quantity =models.CharField(max_length=20,default=1)

    def __str__(self):
        return str(self.name)