from rest_framework import generics, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Location
from .serializers import LocationSerializer


class LocationView(generics.ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = (permissions.AllowAny,)    
    authentication_classes = (JSONWebTokenAuthentication,)

# Create your views here.
