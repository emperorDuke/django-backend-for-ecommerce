from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class BuyerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='buyer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)

    def __str__(self):
        return self.user