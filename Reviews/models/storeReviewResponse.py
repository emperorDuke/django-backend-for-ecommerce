from django.db import models
from django.conf import settings

from ..models.storeReviews import StoreReview



class StoreResponse (models.Model):
    review = models.OneToOneField(StoreReview, related_name='response', verbose_name='review', on_delete=models.CASCADE, primary_key=True)
    response = models.TextField(max_length=300, blank=True, default='')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='store_review_responses', verbose_name='author', on_delete=models.CASCADE)

    class Meta:
        db_table = 'store_review_response'
    
    def __str__(self):
        return self.response
