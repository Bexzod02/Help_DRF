from django.db import models
from django.utils import timezone


class Product(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=221)
    content = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2, default=99.99)
    created_at = models.DateField(default=timezone.now, null=True)

    @property
    def self_price(self):
        return '%.3f'%(float(self.price) * 0.8)

    def get_dicount(self):
        return "122"


