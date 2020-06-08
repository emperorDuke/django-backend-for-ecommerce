from django.db import models
from django.utils.translation import gettext_lazy as _

from mptt.models import TreeForeignKey

from Stores.models.store import Store

from Category.models import Category


def upload_to(instance, filename):
    store = instance.store
    media_path = 'uploads/%s/attachments/%s' % (store.name, filename)
    return media_path

def product_upload_to(instance, filename):
    store = instance.store
    media_path = 'uploads/%s/%s/ ' % (store.name, filename)
    return media_path

class Product(models.Model):
    """
    Product model
    """
    IN_STOCK = "IN STOCK"  
    OUT_OF_STOCK = "OUT OF STOCK"
    AVAILABILITY = (
        (IN_STOCK, "in stock"),
        (OUT_OF_STOCK, "out of stock")
    )

    store = models.ForeignKey(Store, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(_('product name'), max_length=100, blank=False)
    price = models.DecimalField(_('product price'), blank=False, max_digits=12, decimal_places=2)
    discount = models.DecimalField(_('product discount'), blank=True, max_digits=12, decimal_places=2)
    category = TreeForeignKey(Category, null=True, blank=False, related_name='products', on_delete=models.PROTECT)
    brand = models.CharField(_('product brand'), max_length=50, blank=False)
    availability =  models.CharField(_("availabilty"), max_length=50, choices=AVAILABILITY)
    sku = models.CharField(_('SKU'), max_length=50, blank=True)
    attachment_1 = models.ImageField(upload_to=product_upload_to, blank=False)
    attachment_2 = models.ImageField(upload_to=product_upload_to, blank=True)
    attachment_3 = models.ImageField(upload_to=product_upload_to, blank=True)
    attachment_4 = models.ImageField(upload_to=product_upload_to, blank=True)

    ## product detail ##
    description_text = models.TextField(_('product description'), max_length=200, blank=False)
    description_attachment_1 = models.ImageField(upload_to=upload_to, blank=True)
    description_attachment_2 = models.ImageField(upload_to=upload_to, blank=True)

    ref_no = models.CharField(_('reference no'), max_length=100, default="", blank=True, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'
        ordering = ['-updated_at']
        unique_together = ('store', 'name')

    def __str__ (self):
        return self.name





