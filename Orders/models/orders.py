from django.db import models
from django.utils.translation import gettext_lazy as _

from Users.models import address

from Buyer.models import profile, shipping as s
from Payments.models import Payment, Coupon

from utils.code_generator import generator

from Location.models import Location

class Order(models.Model):

    EN = 'ENROUTE'
    PRC = 'PROCESSING'
    DELVD = 'DELIVERED'
    CAN = 'CANCELLED'

    ORDER_STATUS = (
        (EN, 'Enroute'),
        (PRC, 'Processing'),
        (DELVD, 'Delivered'),
        (CAN, 'Cancelled')
    )

    REQ = 'REQUESTED'
    GR = 'GRANTED'
    NR = "NO_REQUEST"

    REFUNDSTATUS = (
        (REQ ,'Requested'),
        (GR,'Granted'),
        (NR,'No Request'),
    )

    PUS = 'PICKUP_SITE'
    D2D = 'DOOR_2_DOOR'

    DELIVERY_METHOD = (
        (PUS, 'Pick-up sites'),
        (D2D, 'Door-to-Door delivery')
    )

    PAYNOW = 'PAYONW'
    PAYONDELVY = 'PAYONDELVY'
    NOPAY = 'NOPAY'

    PAYMENT_METHODS = (
        (PAYNOW, 'pay now'),
        (PAYONDELVY, 'Pay on delivery'),
        (NOPAY, 'No payment')
    )

    buyer = models.ForeignKey(profile.Profile, related_name='orders', verbose_name='buyer', on_delete=models.CASCADE)
    ref_no = models.CharField(_('reference no'), blank=False, max_length=50, unique=True, default='4f55g5')
    shipping_detail = models.ForeignKey(s.Shipping, related_name='orders', blank=True, null=True, on_delete=models.SET_NULL)
    order_status = models.CharField(_('order status'), max_length=50, choices=ORDER_STATUS, blank=False, default=PRC)
    refund_status = models.CharField(_('refund status'), max_length=50, choices=REFUNDSTATUS, blank=False, default=REQ)
    coupons = models.ManyToManyField(Coupon, related_name="orders", verbose_name="coupon")
    payment_method = models.CharField(_('payment method'), choices=PAYMENT_METHODS, max_length=20, blank=False, default=NOPAY)
    delivery_method = models.CharField(_('delivery method'), choices=DELIVERY_METHOD, max_length=50, blank=False, default=D2D)
    pickup_site = models.ForeignKey(Location, blank=True, null=True, on_delete=models.SET_NULL)
    payment = models.OneToOneField(Payment, verbose_name=_('payment'), related_name='order', null=True, on_delete=models.SET_NULL)
    ordered_at = models.DateTimeField(_('date added'), auto_now_add=True)
    updated_at = models.DateTimeField(_('date updated'), auto_now=True)

    class Meta:
        ordering = ['-ordered_at']
        verbose_name_plural = 'Orders'
        db_table = 'Order'

    def __str__(self):
        return self.ref_no

    def save(self, *args, **kwargs):
        self.ref_no = generator(self)
        super(Order, self).save(*args, **kwargs)
    
    
