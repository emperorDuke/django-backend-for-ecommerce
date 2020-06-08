from django.db import models

from .product import Product


def upload_to(instance, filename):
    store = instance.attribute.product.store
    media_path = 'uploads/%s/attachments/%s/' % (store.name, filename)
    return media_path

class Attribute(models.Model):
    product = models.ForeignKey(Product, related_name='attributes', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)

    class Meta:
        unique_together=('product', 'name')
    
    def __str__(self):
        return self.name



class Variation(models.Model):
    attribute = models.ForeignKey(Attribute, related_name='variants', on_delete=models.CASCADE)
    vendor_metric = models.CharField(max_length=50, blank=False)
    metric_verbose_name = models.CharField(max_length=50, blank=True)
    attachment = models.ImageField(upload_to=upload_to, blank=True)

    class Meta:
        unique_together=('attribute', 'vendor_metric')

    def __str__(self):
        return self.vendor_metric

    
