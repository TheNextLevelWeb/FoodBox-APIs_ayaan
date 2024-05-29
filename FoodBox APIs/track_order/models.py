from django.db import models


class TrackOrder(models.Model):
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number
