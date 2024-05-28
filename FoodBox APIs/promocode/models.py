from django.db import models
from django.utils import timezone


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return self.code
