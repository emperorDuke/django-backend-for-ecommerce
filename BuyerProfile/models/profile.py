from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from Products.models.product import Product
from Stores.models.store import Store

class BuyerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='buyer', on_delete=models.CASCADE)
    items_viewed = models.ManyToManyField(Product, blank=True, related_name='users_viewed')
    wish_list = models.ManyToManyField(Product, blank=True, related_name='users_wishlist')
    stores_followed = models.ManyToManyField(Store, related_name='users_following', blank=True)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)

    def __str__(self):
        return self.user