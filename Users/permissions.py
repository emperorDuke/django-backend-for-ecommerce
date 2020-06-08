from rest_framework import permissions

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


from Stores.models.store import Store
from BuyerProfile.models import BuyerProfile


def create_user_permissions(args: str):
    """
    create permission for different category of users
    `seller`, `buyer`, `premium_user`, `free_user`

    """

    if args == 'seller':

        if not Permission.objects.filter(codename='can_sell').exists():

            content_type = ContentType.objects.get_for_model(Store)

            can_sell_permission = Permission.objects.create(
                codename='can_sell', name='Can sell', content_type=content_type)

            seller_group = Group.objects.create(name='sellers')

            seller_group.permissions.add(can_sell_permission)

    elif args == 'buyer':

        if not Permission.objects.filter(codename='can_buy').exists():

            content_type = ContentType.objects.get_for_model(BuyerProfile)

            can_buy_permission = Permission.objects.create(
                codename='can_buy', name='Can buy', content_type=content_type)

            buyer_group = Group.objects.create(name='buyers')

            buyer_group.permissions.add(can_buy_permission)

    elif args == 'premium_user':

        if not Permission.objects.filter(codename='has_full_features').exists():

            content_type = ContentType.objects.get_for_model(get_user_model())

            has_full_features = Permission.objects.create(
                codename='has_full_features', name='Has full features', content_type=content_type)

            premium_user = Group.objects.create(name='premium_users')

            premium_user.permissions.add(has_full_features)

    elif args == 'free_user':

        if not Permission.objects.filter(codename='has_limited_features').exists():

            content_type = ContentType.objects.get_for_model(get_user_model())

            has_limited_features = Permission.objects.create(
                codename='has_limited_features', name='Has limited features', content_type=content_type)

            free_user = Group.objects.create(name='free_users')

            free_user.permissions.add(has_limited_features)

    else:
        None


class IsAccountOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj == request.user

class IsSeller(permissions.BasePermission):

    def has_permission(self, request, view):

        return request.user.groups.filter(name='sellers').exists()


class IsBuyer(permissions.BasePermission):

    def has_permission(self, request, view):

        return request.user.groups.filter(name='buyers').exists()
