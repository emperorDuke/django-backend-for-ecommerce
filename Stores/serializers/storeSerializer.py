from rest_framework import serializers

from ..models.store import Store

from Users.models.address import Address
from Users.serializers.userSerializer import AddressSerializer
from Users.serializers.sellerSerializer import SellerSerializer

from Adverts.serializers import AdvertSerializer

from Ratings.serializers.ratingSerializer import StoreRatingSerializer


class StoreSerializer(serializers.ModelSerializer):

    rating = StoreRatingSerializer(read_only=True)
    adverts = AdvertSerializer(read_only=True)
    address = AddressSerializer(required=True)
    ref_no = serializers.CharField(read_only=True)
    merchant = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Store
        fields = (
            'id',
            'merchant',
            'logo',
            'name',
            'rating',
            'adverts',
            'address',
            'ref_no',
            'address'
        )
        validators = []

    def create(self, validated_data):
        address = validated_data.pop('address', None)
        address_obj = Address.objects.create(**address)
        return Store.objects.create(
            merchant=self.context['request'].user,
            address=address_obj,
            **validated_data
        )

    def update(self, instance, validated_data):
        if 'address' in validated_data:
            address = validated_data.pop('address')
            address_instance = getattr(instance, 'address', None)
            for key, value in address.items():
                setattr(address_instance, key, value)
            address_instance.save()

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
