from django.contrib import admin
from .models import profile, shipping


admin.site.register(profile.Profile)
admin.site.register(shipping.Shipping)

# Register your models here.
