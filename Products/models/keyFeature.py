from django.db import models
from django.utils.translation import gettext_lazy as _

from .product import Product


class KeyFeature(models.Model):
    product = models.ForeignKey(Product, related_name='key_features', verbose_name='product', on_delete=models.CASCADE)
    feature = models.CharField(_('key feature'), max_length=50, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'key_feature'
        verbose_name_plural = 'key_features'
        unique_together = ('product', 'feature')

    def __str__(self):
        return self.feature
