from django.shortcuts import get_object_or_404

from .models.product import Product

from rest_framework import permissions


class AllowClientsWithXHeader(permissions.BasePermission):

    header = 'ANON_USER_43556'

    def has_permission(self, request, view):

        x_header = request.Meta['X_CLIENTS_HEADER']

        return x_header == self.header

class IsSellerProduct(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        productPk = view.kwargs.get('pk', None)

        user_product = request.user.store.products.get(pk=productPk)

        return obj == user_product

class IsProductAttribute(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        products_qs = request.user.store.products.all()

        for product_obj in products_qs:
            if product_obj == obj.product:
                return True
        
        return False


class IsSellerProductMeta(permissions.BasePermission):

    def has_permission(self, request, view):
        
        productPk = view.kwargs.get('pk')
        product_obj = get_object_or_404(Product, pk=productPk)

        spec_obj = getattr(product_obj, 'specifications', None)
        key_features_obj = getattr(product_obj, 'key_features', None)

        user_spec = request.user.store.products.get(pk=productPk).specifications
        user_key_features = request.user.store.products.get(pk=productPk).key_features

        return spec_obj == user_spec and key_features_obj == user_key_features


        