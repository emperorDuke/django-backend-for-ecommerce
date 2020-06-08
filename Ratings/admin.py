from django.contrib import admin

from .models.storeRating import StoreRating
from .models.productRating import ProductRating

# Register your models here.


admin.site.register(StoreRating)
admin.site.register(ProductRating)