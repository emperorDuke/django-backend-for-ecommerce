from rest_framework import viewsets, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from Users.permissions import IsSeller

from .serializers import SponsoredProductSerializer, SponsoredStoreSerializer
from . models import SponsoredProduct, SponsoredStore


class SponsoredProductViewset(viewsets.ModelViewSet):
    serializer_class = SponsoredProductSerializer
    queryset = SponsoredProduct.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, IsSeller]
        else:
            permission_classes = [permissions.IsAuthenticated, IsSeller]

        return [permission() for permission in permission_classes]


class SponsoredStoreViewset(viewsets.ModelViewSet):
    serializer_class = SponsoredStoreSerializer
    queryset = SponsoredStore.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, IsSeller]
        else:
            permission_classes = [permissions.IsAuthenticated, IsSeller]

        return [permission() for permission in permission_classes]
