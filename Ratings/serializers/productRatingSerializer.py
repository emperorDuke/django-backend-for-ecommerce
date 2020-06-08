from rest_framework import serializers

from ..models.productRating import ProductRating

from .ratingSerializer import StoreRatingSerializer



class ProductRatingSerializer(StoreRatingSerializer):

    class Meta(StoreRatingSerializer.Meta):
        model = ProductRating
 