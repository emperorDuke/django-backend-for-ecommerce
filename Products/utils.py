from random import choices
from functools import reduce

from Category.models import Category


class L(object):
    """
    It generates lisitngs automatically
    """

    _lookups = {'latest deals': '-added_at'}
    _level = 1

    def __init__(self, product_qs, serializer):
        self._product_qs = product_qs
        self._serializer = serializer

    def _get_random_categories(self, lookup):
        self._random_categories = choices(lookup, k=2)

    def _get_categories(self):
        category_qs = Category.objects.filter(level=self._level).all()

        if not hasattr(self, '_random_categories'):
            self._get_random_categories(list(category_qs))

    def _get_products(self, qs, container):
        for category in self._random_categories:
            children = list(category.get_children())

            product_qs = [qs.filter(category=child) for child in children]
            product_qs = reduce(lambda a, b: a.union(b), product_qs)

            serializer = self._serializer(product_qs, many=True)
            container.append({category.name: serializer.data})

    def _insert_constant_features(self, qs):
        listings = []

        for key, lookup in self._lookups.items():
            product_qs = qs.order_by(lookup).all()[:10]
            serializer = self._serializer(product_qs, many=True)
            listings.append({key: serializer.data})

        self._get_products(qs, listings)
        self._listings = listings

    @property
    def listings(self):
        """
        Product listings
        """
        if not hasattr(self, '_listings'):
            self._get_categories()
            self._insert_constant_features(self._product_qs)

        return self._listings
