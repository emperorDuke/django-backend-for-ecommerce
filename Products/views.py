from django.shortcuts import get_object_or_404
from django.db.models import F, Prefetch

from rest_framework import permissions, viewsets, status, renderers
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.decorators import action

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from drf_nested_forms.parsers import NestedMultiPartParser

from Category.utils import Item
from Category.filters import CategoryFilter

from Users.permissions import IsSeller

from .models.product import Product
from .models.itemAttribute import Attribute

from .permissions import IsSellerProduct, IsSellerProductMeta, IsProductAttribute
from .filters import ProductFilter, AttributeFilter

from .serializers.productSerializer import ProductSerializer
from .serializers.itemAttributeSerializer import AttributeSerializer
from .serializers.metaSerializer import MetaSerializer, get_instance

from .utils import L


class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related(
        Prefetch('attributes', to_attr='i_attributes'),
        Prefetch('attributes__variants', to_attr='i_variants')
    ).all()

    authentication_classes = (JSONWebTokenAuthentication,)
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = ProductSerializer

    def filter_queryset(self, queryset):
        item = Item(queryset)
        filter_backends = []

        if not bool(self.request.query_params):
            return queryset.order_by('-added_at')
        elif 'category' in self.request.query_params:
            filter_backends.append(CategoryFilter)
        elif item.common_key(item.filters, self.request.query_params):
            filter_backends.append(ProductFilter)
        elif item.common_key(item.attributes, self.request.query_params):
            filter_backends.append(AttributeFilter)
        else:
            pass

        for backend in filter_backends:
            queryset = backend().filter_queryset(self.request, queryset, view=self)

        return queryset

    def get_permissions(self):

        condition = (
            self.action == 'list',
            self.action == 'retrieve',
            self.action == 'listings',
            self.action == 'recently_viewed',
            self.action == 'is_viewed'
        )

        if any(condition):
            permission_classes = [permissions.AllowAny]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, IsSeller]
        else:
            permission_classes = [permissions.IsAuthenticated, IsSeller, IsSellerProduct]

        return [permission() for permission in permission_classes]

    @action(detail=False)
    def recently_viewed(self, request):
        product_queryset = self.get_queryset().annotate(
            recently_viewed=F('viewed__viewed_at')).order_by('-recently_viewed')[:20]
        serializer = self.get_serializer(product_queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def is_viewed(self, request, pk=None):
        product_obj = self.get_object()
        recent_activity = product_obj.viewed
        recent_activity.n_views = F('n_views') + 1
        recent_activity.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=False)
    def listings(self, request):
        l = L(self.get_queryset(), self.get_serializer)
        return Response(data=l.listings, status=status.HTTP_200_OK)


#####################################################################
##                                                                 ##
##                                                                 ##
#####################################################################


class AttributeView(viewsets.GenericViewSet):
    serializer_class = AttributeSerializer
    queryset = Attribute.objects.prefetch_related(
        Prefetch('variants', to_attr='i_variants')).all()
    parser_classes = (NestedMultiPartParser, FormParser)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, IsSeller, IsSellerProduct]

        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        attributes = getattr(product, 'attributes', [])
        serializer = self.get_serializer(attributes, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


#######################################################################
##                                                                   ##
##                                                                   ##
#######################################################################

class ProductMetaView(viewsets.ViewSet):
    parser_classes = (NestedMultiPartParser, FormParser)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated, IsSeller]

        return [permission() for permission in permission_classes]

    def create(self, request):
        serializer = MetaSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        instance = get_instance(pk)
        serializer = MetaSerializer(instance)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        instance = get_instance(pk)
        serializer = MetaSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
