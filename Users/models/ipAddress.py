from django.db import models
from Products.models.product import Product


class IPaddress(models.Model):

    WHITELIST = 'WHITELIST'
    BLACKLIST = 'BLACKLIST'

    STATUS = (
        (WHITELIST, 'white-list'),
        (BLACKLIST, 'black-list')
    )
    
    ip_address = models.IPAddressField()
    status = models.CharField(choices=STATUS, blank=True, default=WHITELIST)
    items_viewed = models.ManyToManyField(Product)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ip_address'

    def __str__(self):
        return self.ip_address