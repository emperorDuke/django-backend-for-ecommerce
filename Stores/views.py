from django.db.models import F

from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import action

from drf_nested_forms.parsers import NestedMultiPartParser

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers.storeSerializer import StoreSerializer, AdvertSerializer
from .models.store import Store, Advert
from .permissions import IsAdvertOwner

from Users.permissions import IsSeller


class StoreView(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    parser_classes = (NestedMultiPartParser, FormParser)
    serializer_class = StoreSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'locations':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, IsSeller]

        return [permission() for permission in permission_classes]

    @action(detail=False)
    def locations(self, request):
        states = self.get_queryset().annotate(
            state=F('address__state')).values_list('state')
        return Response(data=list(set(states)), status=status.HTTP_200_OK)




class Advert_view (viewsets.ModelViewSet):
    queryset = Advert.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AdvertSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated, IsSeller]
        else:
            permission_classes = [permissions.IsAuthenticated, IsSeller, IsAdvertOwner]
        
        return [permission() for permission in permission_classes]
