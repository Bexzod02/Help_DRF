from rest_framework import serializers

from product.models import Product


def validate_title(self, value):
    qs = Product.objects.filter(title__iexact=value)
    if qs.exists():
        raise serializers.ValidationError('Already in use')
    return value