from django.db import models

from .rating import Rating

from Products.models.product import Product

class ProductRating (Rating):
    product = models.OneToOneField(Product, related_name='rating', verbose_name='product', on_delete=models.CASCADE, primary_key=True)

    class Meta(Rating.Meta):
        db_table = 'product_ratings'
   
    
    def __str__ (self):
        return self.rating_average
