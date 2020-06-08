from django.utils import timezone

from rest_framework import serializers

from .models import SponsoredProduct, SponsoredStore, AdsPlan

from Products.models.product import Product
from Payments.serializer import PaymentSerializer
from Products.serializers.productSerializer import ProductSerializer

from Stores.serializers.storeSerializer import StoreSerializer
from Stores.models.store import Store


class AdsPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsPlan
        fields = '__all__'


class SponsoredItemSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)
    plan = AdsPlanSerializer(read_only=True)

    item_id = serializers.IntegerField(required=False)
    ads_plan = serializers.IntegerField(required=False)
    start_sub = serializers.BooleanField(required=False, default=False)

    def update(self, instance, validated_data):
        start_sub = validated_data.pop('start_sub', None)

        if bool(start_sub):
            setattr(instance, 'start_at', timezone.now())
            instance.save()

        return instance

    def to_representation(self, instance):
        instance.check_or_set_expired()

        self.fields.pop('item_id', None)
        self.fields.pop('ads_plan', None)
        self.fields.pop('start_sub', None)

        ret = super().to_representation(instance)
        return ret


class SponsoredProductSerializer(SponsoredItemSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = SponsoredProduct
        fields = (
            'product',
            'payment',
            'plan',
            'has_expired'
            'start_at',
            'ref_no'
            'status',
            'item_id',
            'ads_plan',
            'start_sub'
        )

    def create(self, validated_data):
        product_id = validated_data.get('item_id', None)
        plan_id = validated_data.get('ads_plan', None)

        if product_id and plan_id:
            product_obj = Product.objects.get(pk=product_id)
            ads_plan = AdsPlan.objects.get(pk=plan_id)

            payment = Payment.objects.create(
                amount=ads_plan.amount,
                user=self.context['request'].user
            )

            return SponsoredProduct.objects.create(
                product=product_obj,
                start_at=timezone.now(),
                plan=ads_plan,
                payment=payment
            )


class SponsoredStoreSerializer(SponsoredItemSerializer):
    store = StoreSerializer(read_only=True)

    class Meta:
        model = SponsoredStore
        fields = (
            'store',
            'payment',
            'plan',
            'has_expired'
            'start_at',
            'ref_no'
            'status',
            'item_id',
            'ads_plan',
            'start_sub'
        )

    def create(self, validated_data):
        store_id = validated_data.get('item_id', None)
        plan_id = validated_data.get('ads_plan', None)

        if store_id and plan_id:
            store_obj = Store.objects.get(pk=store_id)
            ads_plan = AdsPlan.objects.get(pk=plan_id)

            payment = Payment.objects.create(
                amount=ads_plan.amount,
                user=self.context['request'].user
            )

            return SponsoredStore.objects.create(
                store=store_obj,
                start_at=timezone.now(),
                plan=ads_plan,
                payment=payment
            )
