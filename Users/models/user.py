from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import PermissionsMixin

from ..userManager import MyUserManager
from .address import Address

from phonenumber_field.modelfields import PhoneNumberField

from rest_framework_jwt.settings import api_settings


class MyUser(AbstractBaseUser, PermissionsMixin):

    SELLER = "SELLER"
    BUYER = "BUYER"
    GUEST = "GUEST"
    ADMIN = "ADMIN"
    USERS = (
        (SELLER, "seller"),
        (BUYER, "buyer"),
        (GUEST, "guest"),
        (ADMIN, "admin")
    )

    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=False)
    middle_name = models.CharField(_('middle name'), max_length=50, blank=True, default='')
    last_name = models.CharField(_('last name'), max_length=50, blank=False)
    phone_number = PhoneNumberField(_('Phone number'), blank=False, unique=True)
    user_type = models.CharField(_("type of user"), max_length=10, choices=USERS, default=GUEST, blank=False)
    is_staff = models.BooleanField(_('staff'), default=False)
    is_active = models.BooleanField(_('active'), default=False)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True)

    objects = MyUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']
    
   
    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()
        
    def get_full_name(self):
        full_name = '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
        return full_name.strip()

    @property
    def get_short_name(self):
        short_name = self.first_name
        return short_name
    
    def _generate_jwt_token(self):

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(self)
        token = jwt_encode_handler(payload)

        return token
