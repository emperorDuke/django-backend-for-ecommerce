from rest_framework import serializers

from .models.shipping_detail import ShippingDetail
from .models.profile import BuyerProfile

from Users.serializers.userSerializer import AddressSerializer
from Users.models.address import Address


class ShippingDetailSerailizer(serializers.ModelSerializer):

    address = AddressSerializer()
    buyer = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ShippingDetail
        fields = '__all__'
        validators = []

    
    def get_buyer_obj(self):
        user = self.context['request'].user
        return BuyerProfile.objects.get(user=user)

    def create(self, validated_data):
        buyer = self.get_buyer_obj()
        address = validated_data.pop('address')
        address_obj = Address.objects.create(**address)

        ShippingDetail.objects.filter(
            buyer=buyer, default=True).update(default=False)

        shipping_detail_obj = ShippingDetail.objects.create(
            buyer=buyer,
            address=address_obj,
            default=True,
            **validated_data
        )

        return shipping_detail_obj

    def update(self, instance, validated_data):
        buyer = self.get_buyer_obj()

        if 'address' in validated_data:
            address_instance = getattr(instance, 'address', None)
            address = validated_data.pop('address')
            for key, value in address.items():
                setattr(address_instance, key, value)
                address_instance.save()

        if 'default' in validated_data:
            default = validated_data.pop('default')
            ShippingDetail.objects.filter(
                buyer=buyer, default=True).update(default=False)
            setattr(instance, 'default', default)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
