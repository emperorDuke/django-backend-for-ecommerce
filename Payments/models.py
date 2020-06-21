from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from BuyerProfile.models.profile import BuyerProfile

from utils.code_generator import generator


class Payment(models.Model):
    PAID = 'paid'
    NOT_PAID = 'not paid'

    PAYMENT_STATUS = (
        (PAID, 'PAID'),
        (NOT_PAID, 'NOT_PAID')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders',
                             verbose_name='user', on_delete=models.CASCADE)
    ref_no = models.CharField(_('reference number'),
                              max_length=50, unique=True, default='dfr44f')
    amount = models.FloatField()
    status = models.CharField(_('payment status'), max_length=50,
                              choices=PAYMENT_STATUS, blank=False, default=NOT_PAID)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.buyer.user.name

    def save(self, *args, **kwargs):
        self.ref_no = generator(self)
        super(Payment, self).save(*args, **kwargs)


class Coupon(models.Model):
    code = models.CharField(max_length=15, unique=True)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
