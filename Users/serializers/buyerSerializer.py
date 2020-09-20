from .userSerializer import UserSerializer
from BuyerProfile.models.profile import BuyerProfile


class BuyerSerializer(UserSerializer):

    def to_internal_value(self, data):
        data = data.copy()
        data['user_type'] = "BUYER"
        return super().to_internal_value(data)

    def create(self, validated_data):
        user = super().create(validated_data)
        BuyerProfile.objects.create(user=user)
        return user