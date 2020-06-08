from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from .models import Category

from Products.models.product import Product

from .utils import build_categories, Item


class CategoryView(APIView):

    renderer_classes = (JSONRenderer,)

    def get(self, request):
        categories = Category.objects.values()
        built_categories = build_categories(categories)
        return Response(data=built_categories, status=status.HTTP_200_OK)


class FilterView(APIView):

    renderer_classes = (JSONRenderer,)

    def get(self, request, name=None):
        category = Category.objects.get(name=name)
        product_qs = Product.objects.select_related(
            'attributes__variants').filter(category=category)
        item = Item(product_qs)
        return Response(data=item.filters, status=status.HTTP_200_OK)
