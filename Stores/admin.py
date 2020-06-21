from django.contrib import admin

# Register your models here.

from .models.store import Store, Advert


admin.site.register(Store)
admin.site.register(Advert)