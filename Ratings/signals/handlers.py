from django.dispatch import receiver
from django.db.models.signals import post_save

from ..models.storeRating import StoreRating
from ..models.productRating import ProductRating

from ..utils import calculate_avg

@receiver(post_save, sender=StoreRating)
def update_store_rating(sender, instance, *args, **kwargs):

    if not instance.n_votes is 0:
        avg = calculate_avg(instance)
        StoreRating.objects.filter(store=instance.store).update(average_rating=avg)


@receiver(post_save, sender=ProductRating)
def update_product_rating(sender, instance, *args, **kwargs):

    if not instance.n_votes is 0:
        avg = calculate_avg(instance)
        ProductRating.objects.filter(product=instance.product).update(average_rating=avg)

    



