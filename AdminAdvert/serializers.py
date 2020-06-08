from rest_framework import serializers

from .models import AdminAdvert


class AdminAdvertSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdminAdvert
        fields='__all__'
        validators = []