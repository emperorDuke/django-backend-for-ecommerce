from rest_framework import serializers

from .userSerializer import UserSerializer, AddressSerializer
from ..models.address import Address

from BuyerProfile.models.profile import BuyerProfile
from BuyerProfile.models.shipping_detail import ShippingDetail


class BuyerSerializer(UserSerializer):

    address = AddressSerializer(required=True)

    def to_internal_value(self, data):
        data = data.copy()
        data['user_type'] = "BUYER"
        return super().to_internal_value(data)

    class Meta(UserSerializer.Meta):
        fields = (
            'first_name',
            'middle_name',
            'last_name',
            'email',
            'phone_number',
            'address',
            'user_type',
            'password'
        )

    def create(self, validated_data):
        address = validated_data.pop('address', None)
        address_obj = Address.objects.create(**address)
        user = super().create(validated_data)
        ShippingDetail.objects.create(
            buyer=user.buyerprofile,
            first_name=validated_data.get('first_name'),
            middle_name=validated_data.get('middle_name'),
            last_name=validated_data.get('last_name'),
            phone_number=validated_data.get('phone_number'),
            address=address_obj,
            default=True
        )
        return user

    def to_representation(self, instance):
        self.fields.pop('address', None)
        return super().to_representation(instance)
