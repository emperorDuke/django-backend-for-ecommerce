from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions, status

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers.productReviewSerializer import ProductReviewSerializer
from .serializers.productReviewResponseSerializer import ProductReviewResSerializer
from .serializers.storeReviewSerializer import StoreReviewSerializer
from .serializers.storeReviewResponseSerializer import StoreReviewResponseSerializer

from .models.productReviews import ProductReview
from .models.productReviewResponse import ProductReviewResponse
from .models.storeReviews import StoreReview
from .models.storeReviewResponse import StoreResponse

from Users.permissions import IsAccountOwner, IsSeller, IsBuyer

from Stores.models.store import Store
from Products.models.product import Product


# Create your views here.
class StorePostReview(generics.CreateAPIView):
    
    queryset = StoreReview.objects.all()
    serializer_class = StoreReviewSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsBuyer)

class StoreGetReview(generics.ListAPIView):
    
    queryset = StoreReview.objects.all()
    serializer_class = StoreReviewSerializer
    permission_classes = (permissions.AllowAny,)
    
    def list(self, request, storePk=None):
        review_set = get_object_or_404(Store, pk=storePk).reviews
        serializer = self.get_serializer(review_set, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class StoreRespondToReview(generics.CreateAPIView):
    
    queryset = StoreResponse.objects.all()
    serializer_class = StoreReviewResponseSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsSeller,)

class ProductPostReview(generics.CreateAPIView):
    
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsBuyer,)



class ProductGetReview(generics.ListAPIView):
    
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = (permissions.AllowAny,)

    def list(self, request, productPk=None):
        review_set = get_object_or_404(Product, pk=productPk).reviews
        serializer = self.get_serializer(review_set, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProductRespondToReview(generics.CreateAPIView):
    
    queryset = ProductReviewResponse.objects.all()
    serializer_class = ProductReviewResSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsSeller, IsAccountOwner)





