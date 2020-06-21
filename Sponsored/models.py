from datetime import timedelta

from django.db import models
from django.utils import timezone

from Stores.models.store import Store
from Payments.models import Payment
from Products.models.product import Product

from utils.code_generator import generator

# Create your models here.


class AdsPlan(models.Model):
    name = models.CharField(max_length=50, blank=True, default="")
    amount = models.FloatField()
    duration = models.PositiveIntegerField('duration in days', default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    ref_no = models.CharField(
        'reference number', max_length=50, unique=True, default='dfr44f')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.ref_no = generator(self)
        super(AdsPlan, self).save(*args, **kwargs)


class Ads(models.Model):

    S = 'SUCCESSFUL'
    F = 'FAILED'
    P = 'PROCESSING'

    STATUS = (
        (P, 'processing'),
        (S, 'process successful'),
        (F, 'process failed')
    )

    start_at = models.DateTimeField('sponsorship will start at', blank=True)
    plan = models.ForeignKey(
        AdsPlan, related_name="%(app_label)s_%(class)s_related", null=True, on_delete=models.SET_NULL)
    payment = models.OneToOneField(
        Payment, related_name="%(app_label)s_%(class)s_related", null=True, on_delete=models.SET_NULL)
    has_expired = models.BooleanField(default=False)
    status = models.CharField('status', max_length=50,
                              choices=STATUS, default=P)
    ref_no = models.CharField(
        'reference number', max_length=50, unique=True, default='dfr44f')

    def save(self, *args, **kwargs):
        self.ref_no = generator(self)
        super(Ads, self).save(*args, **kwargs)

    def expires_at(self):
        return self.start_at + timedelta(days=self.plan.duration)

    def has_expired(self):
        return timezone.now() == self.expires_at()

    def check_or_set_expired(self):
        if self.has_expired():
            self.has_expired = True
            self.save()

    class Meta:
        abstract = True
        ordering = ['-start_at']


class SponsoredStore(Ads):
    store = models.OneToOneField(Store, null=True, on_delete=models.SET_NULL)

    class Meta(Ads.Meta):
        db_table = 'sponsored_store'
        verbose_name = 'sponsored_store'
        verbose_name_plural = 'sponsored_stores'

    def __str__(self):
        return self.store.name


class SponsoredProduct(Ads):
    product = models.OneToOneField(
        Product, null=True, on_delete=models.SET_NULL)

    class Meta(Ads.Meta):
        db_table = 'sponsored_product'
        verbose_name = 'sponsored_product'
        verbose_name_plural = 'sponsored_products'

    def __str__(self):
        return self.product.name
