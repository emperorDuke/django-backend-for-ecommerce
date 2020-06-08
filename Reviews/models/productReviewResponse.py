from django.db import models
from django.conf import settings

from ..models.productReviews import ProductReview

class ProductReviewResponse (models.Model):
    review = models.OneToOneField(ProductReview, related_name='response', verbose_name='review', on_delete=models.CASCADE, primary_key=True)
    response = models.TextField(max_length=300, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='product_review_responses', verbose_name='seller', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_review_responses'



