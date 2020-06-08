from django.db import models
from django.utils.translation import gettext_lazy as _

from .profile import BuyerProfile
from Users.models.address import Address

from phonenumber_field.modelfields import PhoneNumberField


class ShippingDetail(models.Model):
    buyer = models.ForeignKey(BuyerProfile, related_name='shipping_details', on_delete=models.CASCADE)  
    first_name = models.CharField(_('first name'), max_length=50, blank=False)
    middle_name = models.CharField(_('middle name'), max_length=50, blank=True, default='')
    last_name = models.CharField(_('last name'), max_length=50, blank=False)
    phone_number = PhoneNumberField(_('Phone number'), blank=False)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True)
    default = models.BooleanField(default=False)
    added_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.first_name