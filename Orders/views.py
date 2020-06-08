from rest_framework import permissions, viewsets, parsers
from rest_framework.response import Response

from drf_nested_forms.parsers import NestedMultiPartParser

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from Users.permissions import IsBuyer

from .serializer import OrderSerializer
from .models.orders import Order


class OrderView(viewsets.GenericViewSet):
    queryset = Order.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsBuyer)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = OrderSerializer
    parser_classes = (NestedMultiPartParser, parsers.FormParser)

    def filter_queryset(self, queryset):
        buyer = self.request.user.buyerprofile
        return queryset.filter(buyer=buyer)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=201)

    def list(self, request):
        serializer = self.get_serializer(
            self.filter_queryset(self.get_queryset()),
            many=True
        )
        return Response(data=serializer.data, status=200)

    def retrieve(self, request, pk=None):
        serializer = self.get_serializer(self.get_object())
        return Response(data=serializer.data, status=200)

    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(
            self.get_object(), data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=200)
