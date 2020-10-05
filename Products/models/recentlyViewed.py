from django.db import models
from django.utils.translation import gettext_lazy as _

from Products.models.product import Product

class Viewed (models.Model):
    product = models.OneToOneField(Product, verbose_name='product', on_delete=models.CASCADE, primary_key=True)
    n_views = models.IntegerField(_('number of views'), blank=True, default=0)
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'viewed'

    def __str__ (self):
        return self.product.name