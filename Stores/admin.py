from django.contrib import admin

# Register your models here.

from .models.store import Store
from .models.advert import Advert


admin.site.register(Store)
admin.site.register(Advert)