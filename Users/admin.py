from django.contrib import admin

from .models import user, address

admin.site.register(user.MyUser)
admin.site.register(address.Address)
