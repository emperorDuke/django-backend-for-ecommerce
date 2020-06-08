from django.shortcuts import get_object_or_404
from django.db.models import F

from rest_framework import serializers

from ..models.storeRating import StoreRating

from Stores.models.store import Store

class StoreRatingSerializer(serializers.ModelSerializer):

    n_stars = serializers.IntegerField(required=True)

    class Meta:
        model = StoreRating
        fields = (
            'n_stars', 
            'average_rating', 
            'n_one_star_votes',
            'n_two_stars_votes',
            'n_three_stars_votes',
            'n_four_stars_votes',
            'n_five_stars_votes',
            'n_votes'
            )

        read_only_fields = ('n_votes', 'average_rating')
    
    def validate(self, data):
        if data['n_stars'] > 5:
            raise serializers.ValidationError (
                'There cannot be a rating above 5'
            )
        return super().validate(data)

    

    def update(self, instance, validated_data):

        value = validated_data.pop('n_stars', None)

        if  value == 1:
            instance.n_one_star_votes = F('n_one_star_votes') + 1
        elif value == 2:
            instance.n_two_stars_votes = F('n_two_stars_votes') + 1
        elif value == 3:
            instance.n_three_stars_votes = F('n_three_stars_votes') + 1
        elif value == 4:
            instance.n_four_stars_votes = F('n_four_stars_votes') + 1
        elif value == 5:
            instance.n_five_stars_votes = F('n_five_stars_votes') + 1
        else:
            None
            

        instance.n_votes = F('n_one_star_votes') + F('n_two_stars_votes') + F('n_three_stars_votes') + F('n_four_stars_votes') + F('n_five_stars_votes') + 1

        instance.save()

        instance.refresh_from_db()

        return instance

    def to_representation(self, instance):
        self.fields.pop("n_stars", None)
        ret = super().to_representation(instance)
        return ret

       





    
