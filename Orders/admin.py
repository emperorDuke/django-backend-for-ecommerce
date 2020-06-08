from django.contrib import admin
from .models import ordered_item, orders

# Register your models here.

admin.site.register(ordered_item.OrderedItem)
admin.site.register(orders.Order)
