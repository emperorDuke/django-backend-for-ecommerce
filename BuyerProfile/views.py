from rest_framework import viewsets, permissions, parsers
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from drf_nested_forms.parsers import NestedMultiPartParser, NestedJSONParser

from .models import ShippingDetail
from .serializers import ShippingDetailSerailizer

from Users.permissions import IsBuyer


class ShippingDetailView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsBuyer)
    parser_classes = (NestedMultiPartParser, NestedJSONParser, parsers.FormParser)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = ShippingDetailSerailizer
    queryset = ShippingDetail.objects.all()

    def filter_queryset(self, queryset):
        buyer = self.request.user.buyerprofile
        return queryset.filter(buyer=buyer)
