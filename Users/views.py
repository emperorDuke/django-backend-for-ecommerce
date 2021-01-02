from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from drf_nested_forms.parsers import NestedJSONParser, NestedMultiPartParser

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMultiAlternatives
from django.template import loader

from .serializers.sellerSerializer import SellerSerializer
from .serializers.buyerSerializer import BuyerSerializer
from .permissions import IsAccountOwner, IsBuyer
from .validations import login

from Buyer.serializers import ShippingSerailizer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    authentication_classes = (JSONWebTokenAuthentication,)
    parser_classes = (NestedJSONParser, NestedMultiPartParser, FormParser)

    def get_serializer_class(self):
        if self.request.version == 'seller':
            return SellerSerializer
        elif self.request.version == 'buyer':
            return BuyerSerializer

    def get_permissions(self):
        if self.action == 'create' or self.action == 'login':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsAccountOwner]
        return [permission() for permission in permission_classes]

    @action(detail=False)
    def address_book(self, request):
        addresses = request.user.profile.shipping_details
        serializer = ShippingSerailizer(addresses, many=True)
        return Response(data=serializer.data, status=200)

    @action(methods=['post'], detail=False)
    def login(self, request):
        data = login(request, self.get_serializer)
        return Response(data=data, status=status.HTTP_200_OK)


class ConfirmPassword(APIView):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    ##############################################
    ## before the user can change password,     ##
    ## current password must be confirmed and   ##
    ## create a one_time password change token  ##
    ##############################################

    def post(self, request):
        user = request.user
        user = user.check_password(request.data['password'])
        if user is True:
            token_generator = default_token_generator
            reset_token = token_generator.make_token(user)
            uid = user.id
            data = {
                'user': {'reset_token': token, 'pk': uid}
            }
            return Response(data=data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ChangePassword(APIView):

    queryset = get_user_model().objects.all()

    ########################################################
    ## handles changing password but password validation  ##
    ## will be carried out at the frontend                ##
    ########################################################

    def post(self, request, pk=None, token=None):

        user_obj = get_object_or_404(self.queryset, pk=pk)

        assert pk is not None and token is not None

        token_generator = default_token_generator

        if user_obj is not None and token_generator.check_token(user_obj, token):
            serializer = self.serializer_class(
                user_obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ForgotPassword(APIView):

    queryset = get_user_model().objects.all()

    ########################################################
    #### user will have to validated email address first ###
    #### before link can be sent                         ###
    ########################################################

    def post(self, request):

        email_data = request.data['email']
        user = get_object_or_404(self.queryset, email=email_data)

        if email_data == user.email:
            if user.is_active and user.has_usable_password():
                token_generator = default_token_generator
                uid64 = urlsafe_base64_encode(force_bytes(user.id))
                token = token_generator.make_token(user)

                context = {
                    'protocol': 'https',
                    'email': user.email,
                    'uid64': uid64,
                    'token': token,
                    'domain': 'www.biddu.com'
                }
                subject_template_name = 'account/password_reset_subject.txt'
                email_template_name = 'account/password_reset_email.txt'
                html_email_template = 'account/password_reset_email.html'

                subject = loader.render_to_string(
                    subject_template_name, context)
                subject = ''.join(subject.spiltlines())

                body = loader.render_to_string(email_template_name, context)

                html_email = loader.render_to_string(
                    html_email_template, context)

                message = EmailMultiAlternatives(
                    subject=subject,
                    body=body,
                    from_email='no_reply@biddu.com',
                    to=[user.email]
                )
                message.attach_alternative(html_email, "text/html")
                message.send()

                return Response(data={'Message: Email confirmation successful'}, status=status.HTTP_200_OK)

            return Response(data={'Message: User deactivated'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(data={'Message': 'Email not Found!'}, status=status.HTTP_404_NOT_FOUND)


class ConfirmLink(APIView):

    queryset = get_user_model().objects.all()

    ####################################################
    ### confirms the link sent to the user as geniue ###
    ####################################################

    def post(self, request, uidb64, token):

        assert uidb64 is not None and token is not None

        uid = force_text(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(self.queryset, id=uid)
        token_generator = default_token_generator

        if user and token_generator.check_token(user, token):

            if user.is_active == False:
                user.is_active = True
                user.save()
                data = {'token': token, 'pk': uid}
            return Response(data=data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
