from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

from utils.code_generator import generator

from ..models.product import Product
from ..models.recentlyViewed import Viewed

from Ratings.models.productRating import ProductRating

@receiver(post_save, sender=Product)
def create_obj(sender, instance, created, *args, **kwargs):

    if created:
        Viewed.objects.create(product=instance)
        ProductRating.objects.create(product=instance)


@receiver(pre_save, sender=Product)
def create_track_id(sender, instance, *args, **kwargs):
    instance.ref_no = generator(instance)
