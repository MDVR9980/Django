from django.db import models

class Product(models.model):
    name = models.CharField(max_length=12)

class Item(models.Model):
    product = models.ForeignKey(Product, )