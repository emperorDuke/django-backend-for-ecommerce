from django.contrib import admin
from Products import models


# Register your models here.

admin.site.register(models.product.Product)
admin.site.register(models.recentlyViewed.Viewed)
admin.site.register(models.specification.Specification)
admin.site.register(models.keyFeature.KeyFeature)
admin.site.register(models.itemAttribute.Attribute)
admin.site.register(models.itemAttribute.Variation)