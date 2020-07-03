from django.db import models

from Products.models.product import Product
from ..models.reviews import Reviews

class ProductReview (Reviews):
    product = models.ForeignKey(Product, related_name='reviews', verbose_name='product', on_delete=models.CASCADE)

    class Meta(Reviews.Meta):
        db_table = 'product_review'

    def __str__(self):
        return self.review


