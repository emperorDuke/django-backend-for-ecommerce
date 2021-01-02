from rest_framework import viewsets, permissions, parsers
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from drf_nested_forms.parsers import NestedMultiPartParser, NestedJSONParser

from .models import Shipping
from .serializers import ShippingSerailizer

from Users.permissions import IsBuyer


class ShippingView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsBuyer)
    parser_classes = (NestedMultiPartParser, NestedJSONParser, parsers.FormParser)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = ShippingSerailizer
    queryset = Shipping.objects.all()

    def filter_queryset(self, queryset):
        buyer = self.request.user.profile
        return queryset.filter(buyer=buyer)
