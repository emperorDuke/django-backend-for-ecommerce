from rest_framework import serializers

from .models.shipping import Shipping
from .models.profile import Profile

from Users.serializers.userSerializer import AddressSerializer
from Users.models.address import Address


class ShippingSerailizer(serializers.ModelSerializer):
    address = AddressSerializer()
    buyer = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Shipping
        fields = '__all__'
        validators = []

    
    def get_buyer_obj(self):
        user = self.context['request'].user
        return Profile.objects.get(user=user)

    def create(self, validated_data):
        buyer = self.get_buyer_obj()
        address = validated_data.pop('address')
        address_obj = Address.objects.create(**address)

        Shipping.objects.filter(
            buyer=buyer, default=True).update(default=False)

        shipping_detail_obj = Shipping.objects.create(
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
            Shipping.objects.filter(
                buyer=buyer, default=True).update(default=False)
            setattr(instance, 'default', default)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
