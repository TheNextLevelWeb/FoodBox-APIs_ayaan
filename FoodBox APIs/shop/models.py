from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(
        Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    subcategory = models.ForeignKey(
        Subcategory, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
