from django.db.models import Sum

from rest_framework import serializers

from .models.ordered_item import OrderedItem, Order

from Cart.serializer import CartSerializer
from Cart.models import Cart

from Buyer.models.profile import Profile
from Buyer.models.shipping import Shipping
from Buyer.serializers import ShippingSerailizer

from Payments.models import Payment
from Payments.serializer import CouponSerializer, PaymentSerializer

from Location.models import Location
from Location.serializers import LocationSerializer


class OrderItemSerializer(serializers.ModelSerializer):

    order = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField()
    cart_content = CartSerializer(read_only=True)

    class Meta:
        model = OrderedItem
        exclude = ('variants', 'product', 'quantity', 'price')
        validators = []


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(read_only=True, many=True)
    coupons = CouponSerializer(read_only=True)
    payment = PaymentSerializer(read_only=True)
    shipping_detail = ShippingSerailizer(required=False)
    buyer = serializers.PrimaryKeyRelatedField(read_only=True)
    payment_method = serializers.CharField(required=False)
    delivery_method = serializers.CharField(required=False)
    pickup_site = LocationSerializer(required=False)

    class Meta:
        model = Order
        fields = (
            'buyer',
            'items',
            'coupons',
            'payment',
            'order_status',
            'refund_status',
            'shipping_detail',
            'buyer',
            'ordered_at',
            'updated_at',
            'payment_method',
            'delivery_method',
            'pickup_site'
        )

    @staticmethod
    def get_total_amount(instance):
        cart_qs = Cart.objects.filter(buyer=instance)
        return cart_qs.aggregate(amount=Sum('price')).get('amount')

    @staticmethod
    def get_shipping_detail_obj(buyer):
        return Shipping.objects.filter(
            buyer=buyer, default=True).first()

    def get_buyer_obj(self):
        user = self.context['request'].user
        return Profile.objects.get(user=user)

    def create(self, validated_data):
        buyer = self.get_buyer_obj()
        shipping_detail = self.get_shipping_detail_obj(buyer)

        payment = Payment.objects.create(
            amount=self.get_total_amount(buyer),
            user=self.context['request'].user
        )
        order_obj = Order.objects.create(
            buyer=buyer,
            shipping_detail=shipping_detail,
            payment=payment,
            **validated_data
        )

        cart_qs = buyer.cart.all()
        cart_list = []

        for qs in cart_qs:
            temp = {}
            temp['order'] = order_obj
            temp['product'] = qs.product
            temp['quantity'] = qs.quantity
            temp['price'] = qs.price
            temp['name'] = qs.product.name
            temp['cart_content'] = qs

            cart_list.append(temp)

        OrderedItem.objects.bulk_create(
            [
                OrderedItem(**item)
                for item in cart_list
            ]
        )

        order_item_qs = OrderedItem.objects.filter(order=order_obj)

        for item in order_item_qs:
            variants = item.cart_content.variants.all()
            item.variants.set(list(variants))

        return order_obj

    def update(self, instance, validated_data):
        buyer = self.get_buyer_obj()
        shipping_detail = self.get_shipping_detail_obj(buyer)
        delivery = validated_data.pop('delivery_method', None)
        pickup_site = validated_data.pop('pickup_site', None)
        shipping_detail = validated_data.pop('shipping_detail', None)
        serializer = self.fields.get('shipping_detail', None)
        serializer.context['request'] = self.context['request']

        if shipping_detail and 'id' in shipping_detail:
            shipping_obj = getattr(instance, 'shipping_detail')
            shipping_obj = serializer.update(shipping_obj, shipping_detail)
            setattr(instance, 'shipping_detail', shipping_obj)
        elif shipping_detail and 'id' not in shipping_detail:
            shipping_obj = serializer.create(shipping_detail)
            setattr(instance, 'shipping_detail', shipping_obj)

        if delivery and delivery == Order.PUS and pickup_site:
            pickupsite_obj = Location.objects.get(pk=pickup_site.get('id'))
            setattr(instance, 'pickup_site', pickupsite_obj)
            setattr(instance, 'delivery_method', Order.PUS)
        elif delivery and delivery == Order.D2D:
            setattr(instance, 'delivery_method', Order.D2D)
            setattr(instance, 'shipping_detail', shipping_detail)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
