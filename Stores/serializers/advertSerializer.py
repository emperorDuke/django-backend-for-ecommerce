from rest_framework import serializers

from ..models.advert import Advert


class AdvertSerializer (serializers.ModelSerializer):

    class Meta:
        model = Advert
        fields = '__all__'
        validators = []

    def validate(self, data):

        request = self.context['request']

        if request.method == 'post':

            user = request.user

            advert_count = Advert.objects.filter(store=user.store).count()

            if advert_count > 2 and not user.groups.filter(name='premium_user').exists():
                raise serializers.ValidationError(
                    "maximum adverts exceeded for your plan")

        return super().validate(data)