from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db.models import F
from django.shortcuts import get_object_or_404

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import Coupon

from Orders.models.orders import Order


class CouponView(APIView):

    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, order_pk=None):
        code = request.data.get('code', None)

        if code is not None:
            coupon = get_object_or_404(Coupon, code=code)
            order = get_object_or_404(Order, pk=order_pk)

            payment = order.payment

            payment.amount = F('amount') - coupon.amount
            payment.save()

            order.coupons.add(coupon)

            return Response(status=status.HTTP_200_OK)
        
        return Response({'code':'code is not found'}, status=status.HTTP_400_BAD_REQUEST)
