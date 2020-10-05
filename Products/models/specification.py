from django.db import models
from django.utils.translation import gettext_lazy as _

from .product import Product


class Specification (models.Model):
    product = models.ForeignKey(Product, related_name='specifications', verbose_name='product', on_delete=models.CASCADE)
    type = models.CharField(_('specification type'), max_length=100, blank=False, default='')
    value = models.CharField(_('specification content'), max_length=100, blank=False, default='')
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'specification'
        verbose_name_plural = 'specifications'
        unique_together = ('product', 'type', 'value')
        db_table = 'product_specification'

    def __str__(self):
        return '%s_%s: %s' % (self.product.name, self.type, self.value)