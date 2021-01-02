from django.db import models
from django.utils.translation import gettext_lazy as _

from Products.models import product as p, itemAttribute as i
from Buyer.models.profile import Profile

class Cart(models.Model):
    buyer = models.ForeignKey(Profile, related_name='cart', on_delete=models.CASCADE)
    product = models.ForeignKey(p.Product, verbose_name='products', null=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(_('quantity of products'), default=1)
    price = models.DecimalField(_("total price"), blank=False, max_digits=12, decimal_places=2)
    variants = models.ManyToManyField(i.Variation, verbose_name='variants of product')
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)
    

    class Meta:
        db_table = 'Cart'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return self.product.name