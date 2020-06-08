from django.dispatch import receiver
from django.db.models.signals import post_save

from ..models import Category


@receiver(post_save, sender=Category)
def create_track_id(sender, instance, created, *args, **kwargs):
    if created and not instance.track_id:
        children = instance.parent.get_children()
        if children.count() <= 1:
            Category.objects.filter(
                name=instance.name,
                parent=instance.parent
            ).update(
                track_id="{0}-{1}".format(instance.parent.track_id, 1)
            )
        else:
            Category.objects.filter(
                name=instance.name,
                parent=instance.parent
            ).update(
                track_id="{0}-{1}".format(instance.parent.track_id,
                                          children.count())
            )
