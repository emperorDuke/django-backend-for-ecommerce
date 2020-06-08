from rest_framework import serializers

from .models import Payment, Coupon



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        validations = []
        read_only_fields = ('amount',)




class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = '__all__'
        validations = [],
        read_only_fields = ('amount', 'code')



