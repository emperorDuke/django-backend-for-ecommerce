from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from Users.permissions import IsSeller

from .serializers import AdvertSerializer
from .models import Advert
from .permissions import IsAdvertOwner




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

    
