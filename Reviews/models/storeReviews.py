from django.db import models

from ..models.reviews import Reviews
from Stores.models.store import Store


class StoreReview(Reviews):
    store = models.ForeignKey(Store, related_name='reviews', verbose_name='store', on_delete=models.CASCADE)

    class Meta(Reviews.Meta):
        db_table = 'store_review'
        
    def __str__(self):
        return self.review