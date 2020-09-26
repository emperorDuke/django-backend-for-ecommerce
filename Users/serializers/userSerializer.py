from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from django.contrib.auth import get_user_model

from ..models.address import Address

from phonenumber_field.serializerfields import PhoneNumberField

class AddressSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Address
        fields = '__all__'
        validators = []



class UserSerializer(serializers.ModelSerializer):

    phone_number = PhoneNumberField(required=True)
    user_type = serializers.CharField(max_length=10, required=False)

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        return get_user_model().objects.create_user(
            email,
            password,
            **validated_data
        )

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == 'password':
                password = validated_data.pop(key)
                instance.set_password(password)
            setattr(instance, key, value)
        instance.save()
        return instance

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "first_name", 
            "middle_name", 
            "last_name", 
            "phone_number",
            "email",
            "user_type",
            "password"
            )
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('user_type',)
        validators = [
            UniqueTogetherValidator(
                queryset=get_user_model().objects.all(),
                fields=('email', 'phone_number')
            )
        ]


