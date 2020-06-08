from django.shortcuts import get_object_or_404

from rest_framework import serializers

from ..models.storeReviewResponse import StoreResponse
from ..models.storeReviews import StoreReview



class StoreReviewResponseSerializer(serializers.ModelSerializer):

    review = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = StoreResponse
        fields = "__all__"
        validators = []
    
    def get_author (self, obj=None):
        return self.context['request'].user

    def get_review (self, obj=None):
        review_pk = self.context['view'].kwargs.get('reviewPk')
        review_obj = get_object_or_404(StoreReview, pk=review_pk)
        return review_obj

    def to_internal_value(self, data):

        store_reply_sets = self.get_author().store_review_responses

        if store_reply_sets.filter(review=self.get_review()).exists():
            raise serializers.ValidationError(
                {'author':'number of reply per review is exceeded'}
            )

        return super().to_internal_value(data)

    def create (self, validated_data):
        review = self.get_review()
        author = self.get_author()

        return StoreResponse.objects.create (
            review=review,
            author=author,
            **validated_data
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['author'] = instance.author.store.name
        return ret
