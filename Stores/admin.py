from django.contrib import admin

# Register your models here.

from .models.store import Store


admin.site.register(Store)