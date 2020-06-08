from django.db import models
from Stores.models.store import Store
from .rating import Rating

class StoreRating(Rating):
    store = models.OneToOneField(Store, related_name='rating', verbose_name='store', on_delete=models.CASCADE, primary_key=True)

    class Meta(Rating.Meta):
        db_table = 'store_ratings'

    def __str__(self):
        return self.rating_average
    
