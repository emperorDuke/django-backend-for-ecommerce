from django.shortcuts import get_object_or_404

from rest_framework import serializers

from ..models.storeReviews import StoreReview

from .storeReviewResponseSerializer import StoreReviewResponseSerializer

from Stores.models import Store


class StoreReviewSerializer(serializers.ModelSerializer):

    response = StoreReviewResponseSerializer(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    store = serializers.PrimaryKeyRelatedField(read_only=True)


    class Meta:
        model = StoreReview
        fields =  ('id','author','store', 'response','review')
        validators = []

    
    def get_store(self, obj=None):
        storePk = self.context['view'].kwargs.get('storePk')
        store = get_object_or_404(Store, pk=storePk)
        return store

    def get_author(self, obj=None):
        return self.context['request'].user

    def to_internal_value(self, data):
        review_sets = self.get_store().reviews

        if review_sets.filter(author=self.get_author()).exists():
            raise serializers.ValidationError({
                "author":"multiple reviews from this user on the same store"
                })
        
        return super().to_internal_value(data)


    def create(self, validated_data):
        author = self.get_author()
        store = self.get_store()

        return StoreReview.objects.create(
            author=author,
            store=store,
            **validated_data
        )
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['author'] = instance.author.get_short_name
        return ret
