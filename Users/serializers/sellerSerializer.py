from rest_framework import serializers

from .userSerializer import UserSerializer


class SellerSerializer(UserSerializer):

    def to_internal_value(self, data):
        data = data.copy()
        data['user_type'] = "seller"
        return super().to_internal_value(data)
