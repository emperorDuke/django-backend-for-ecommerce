from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from ..models.store import Store

from Ratings.models.storeRating import StoreRating

from utils.code_generator import generator


@receiver(post_save, sender=Store)
def create_other_info(sender, instance, created, *args, **kwargs):
    if created:
        StoreRating.objects.create(store=instance)


@receiver(pre_save, sender=Store)
def create_ref_no(sender, instance, *args, **kwargs):
    instance.ref_no = generator(instance)
