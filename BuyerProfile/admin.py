from django.contrib import admin
from .models import profile, shipping_detail


admin.site.register(profile.BuyerProfile)
admin.site.register(shipping_detail.ShippingDetail)

# Register your models here.
