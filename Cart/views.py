from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from drf_nested_forms.parsers import NestedMultiPartParser, NestedJSONParser

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializer import CartSerializer
from .models import Cart

from Users.permissions import IsBuyer


# Create your views here.

class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, IsBuyer)
    serializer_class = CartSerializer
    parser_classes = (NestedMultiPartParser, NestedJSONParser)

    def filter_queryset(self, queryset):
        buyer = self.request.user.buyerprofile
        return queryset.filter(buyer=buyer)

    def destroy(self, request, pk=None):
        cart_obj = self.get_object()
        order_item_obj = getattr(cart_obj, 'ordereditem', None)

        cart_obj.delete()

        if order_item_obj is not None:
            order_item_obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
