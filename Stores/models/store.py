from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from Users.models.address import Address

def upload_to(instance, filename):
    media_path = 'uploads/{0}/logo/{1}'.format(instance.name, filename)
    return media_path


class Store(models.Model):
    merchant = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to=upload_to, blank=True)
    name = models.CharField(_('store name'), max_length=50, unique=True)
    ref_no = models.CharField(_('reference no'), max_length=100, default="", blank=True, unique=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


def ad_upload_to(instance, filename):
    media_path = "uploads/%s/adverts/%s" % (instance.store.name, filename)
    return media_path
    
    ####
    ####
    ###

class Advert(models.Model):
    store = models.OneToOneField(Store, verbose_name="store", on_delete=models.CASCADE)
    attachment = models.ImageField(upload_to=ad_upload_to, blank=True)
    text = models.TextField(verbose_name='advert text', max_length=100, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'advert'
        verbose_name_plural = 'adverts'
        db_table='store_adverts'
        ordering = ['-updated_at']

    def __str__(self):
        return '%s-%s' % (self.store.name, self.text)