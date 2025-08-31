from django.db import models

class Size(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title

class Color(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    price = models.IntegerField()
    discount = models.SmallIntegerField()
    image = models.ImageField(upload_to="products")
    size = models.ManyToManyField(Size, related_name='products', blank=True, null=True)
    color = models.ManyToManyField(Color, related_name='products')

    # class Meta:

    def __str__(self):
        return self.title
    

class Information(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name="informations")
    text = models.TextField()

    def __str__(self):
        return self.text[:30]