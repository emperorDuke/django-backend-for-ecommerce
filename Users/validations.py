from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from rest_framework import exceptions


def authenticate(**credentials):

    email = credentials.get(get_user_model().USERNAME_FIELD)
    password = credentials.get('password')

    users = get_user_model().objects.all()

    for user in users:
        if user.email == email and user.check_password(password):
            return user

    return None


def login(request, serializer=None):
    """
    validates the request and set the user 
    authentication attribute to True
    """

    email = request.data.get('email')
    password = request.data.get('password')

    if email is None:
        raise AttributeError(
            'An email is required'
        )
    if password is None:
        raise AttributeError(
            'A password is required'
        )

    credentials = {
        get_user_model().USERNAME_FIELD: email,
        'password': password
    }

    user = authenticate(**credentials)

    if user is None:
        raise exceptions.AuthenticationFailed(_('user does not exist'))

    if user.is_active is False:
        raise exceptions.AuthenticationFailed(_('user is not active'))

    return {
        'token': user.token,
        'user': serializer(user, context={'request': request}).data
    }
