from django.contrib import admin

from .models import SponsoredStore, SponsoredProduct, AdsPlan
# Register your models here.
admin.site.register(SponsoredStore)
admin.site.register(SponsoredProduct)
admin.site.register(AdsPlan)
