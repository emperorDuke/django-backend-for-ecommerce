from rest_framework import viewsets, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from Users.permissions import IsSeller

from .serializers import SponsoredProductSerializer, SponsoredStoreSerializer
from . models import SponsoredProduct, SponsoredStore

class SponsoredProductViewset(viewsets.ModelViewSet):
    serializer_class = SponsoredProductSerializer
    queryset = SponsoredProduct.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsSeller)



class SponsoredStoreViewset(viewsets.ModelViewSet):
    serializer_class = SponsoredStoreSerializer
    queryset = SponsoredStore.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsSeller)