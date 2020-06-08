from rest_framework import generics, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import AdminAdvert
from .serializers import AdminAdvertSerializer


class AdminAdvertView(generics.ListAPIView):
    queryset = AdminAdvert.objects.all()
    serializer_class = AdminAdvertSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.AllowAny,)
