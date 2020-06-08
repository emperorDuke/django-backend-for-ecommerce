from django.db import models
from django.utils.translation import gettext_lazy as _

from Products.models import product as p, itemAttribute as i

from .orders import Order
from Cart.models import Cart


class OrderedItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', verbose_name='order', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True)
    product = models.ForeignKey(p.Product, verbose_name='products', null=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(_('quantity of products'), default=1)
    price = models.DecimalField(_("total price"), blank=False, max_digits=12, decimal_places=2, default='0.00')
    variants = models.ManyToManyField(i.Variation, verbose_name='variant of product')
    cart_content = models.OneToOneField(Cart, verbose_name='cart_content', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.product.name
        

    