from django.db import models

from Stores.models.store import Store


def upload_to(instance, filename):
    media_path = "uploads/%s/adverts/%s" % (instance.store.name, filename)
    return media_path

class Advert(models.Model):
    store = models.OneToOneField(Store, verbose_name="store", on_delete=models.CASCADE)
    attachment = models.ImageField(upload_to=upload_to, blank=True)
    text = models.TextField(verbose_name='advert text', max_length=100, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'advert'
        verbose_name_plural = 'adverts'
        db_table='store_adverts'
        ordering = ['-updated_at']