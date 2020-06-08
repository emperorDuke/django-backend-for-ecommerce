from django.db import models
from django.conf import settings


class Reviews (models.Model):
    review = models.TextField(max_length=300, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="%(app_label)s_%(class)s_related", verbose_name='buyer', on_delete=models.CASCADE)

    class Meta:
        abstract=True

