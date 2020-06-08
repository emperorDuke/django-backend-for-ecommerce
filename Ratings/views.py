from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework import generics

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models.storeRating import StoreRating
from .models.productRating import ProductRating

from Products.models import Product
from Stores.models.store import Store

from .serializers.ratingSerializer import StoreRatingSerializer
from .serializers.productRatingSerializer import ProductRatingSerializer

from Users.permissions import IsBuyer




class StoreRatingView (generics.UpdateAPIView):

    queryset = StoreRating.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsBuyer)
    serializer_class = StoreRatingSerializer


class ProductRatingView (generics.UpdateAPIView):

    queryset = ProductRating.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsBuyer)
    serializer_class = ProductRatingSerializer


