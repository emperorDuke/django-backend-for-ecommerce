from rest_framework import viewsets, permissions, parsers
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Location
from .serializers import LocationSerializer

# Create your views here.
class LocationView(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser)

    def get_permissions(self):
        if self.action != 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

