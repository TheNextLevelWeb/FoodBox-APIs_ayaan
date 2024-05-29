from django.db import models


class Cart(models.Model):
    user = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user} - {self.item} - {self.quantity}"
