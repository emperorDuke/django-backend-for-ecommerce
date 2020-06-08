from rest_framework import serializers

from .models.cart import Cart

from BuyerProfile.models.profile import BuyerProfile

from Products.models.itemAttribute import Variation
from Products.serializers.itemAttributeSerializer import VariationSerializer


class CartSerializer(serializers.ModelSerializer):
    variants = VariationSerializer(many=True)
    buyer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'
        validators = []

    def get_data_defaults(self, product_obj=None):
        user_instance = self.context['request'].user
        buyer_profile = BuyerProfile.objects.get(user=user_instance)

        return {
            'product': product_obj,
            'buyer': buyer_profile
        }

    @staticmethod
    def get_variant_list(variants):
        return [
            Variation.objects.get(pk=variant['id'])
            for variant in variants
        ]

    def create(self, validated_data):
        variants = validated_data.pop('variants', None)
        product = validated_data.pop('product', None)

        variant_list = self.get_variant_list(variants)
        data_defaults = self.get_data_defaults(product)

        for key, value in data_defaults.items():
            validated_data[key] = value

        cart_instance = Cart.objects.create(**validated_data)
        cart_instance.variants.set(variant_list)

        return cart_instance

    def update(self, instance, validated_data):
        if 'variants' in validated_data:
            variants = validated_data.pop('variants', None)
            variant_list = self.get_variant_list(variants)
            instance.variants.set(variant_list)

        if validated_data:
            for key, value in validated_data.items():
                setattr(instance, key, value)

        instance.save()

        return instance
