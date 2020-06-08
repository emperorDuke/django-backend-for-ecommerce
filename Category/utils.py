import math, re

from django.db.models import Min, Max


def build_categories(iteratable, level=5):

    pat = re.compile(r'\sand\s')

    def strip(arg=''):
        substrings = re.split(pat, arg)
        return ' & '.join(substrings)

    level_2 = []
    level_1 = []
    level_0 = []

    build_0 = []

    for query in iteratable:
        for key, value in query.items():
            if key == 'level' and value == 2:
                level_2.append(query)
            elif key == 'level' and value == 1:
                level_1.append(query)
            elif key == 'level' and value == 0:
                level_0.append(query)
            else:
                pass

    for i in level_0:
        build_1 = []
        for k_0, v_0 in i.items():
            if k_0 == "id":
                for j in level_1:
                    build_2 = []
                    for k_1, v_1 in j.items():
                        if k_1 == 'parent_id' and v_1 == v_0:
                            for k in level_2:
                                for k_2, v_2 in k.items():
                                    if k_2 == 'parent_id' and v_2 == j["id"]:
                                        build_2.append({
                                            "name": strip(k["name"]),
                                            "id": k["id"],
                                            "children": None
                                        })
                            if build_2:
                                build_1.append({
                                    "name": strip(j["name"]),
                                    "id": j["id"],
                                    "children": build_2
                                })
                if build_1:
                    build_0.append({
                        "name": strip(i["name"]),
                        "id": i["id"],
                        "children": build_1
                    })

    return build_0


class Item(object):
    """
    It generates a collection of filters for the items or products in the db
    and also provides utility functions for handling filters
    """

    def __init__(self, product_qs):
        self._product_qs = product_qs

    @staticmethod
    def common_key(map_1, map_2):
        """
        Returns `True` if the arguments share any key in common
        else `False`
        """
        common_keys = set(map_1) & set(map_2)  # intersection ##
        return bool(common_keys)

    @staticmethod
    def _get_price_ranges(min_price, max_price, n_price_ranges=5):
        """
        get the prices and their intervals
        """
        price_range = max_price / n_price_ranges
        prices = []
        new_min = min_price  # this min value will always increase by one ##
        for _ in range(n_price_ranges):
            prices.append({
                'key': '%s - %s' % (new_min, new_min + price_range),
                'value': 'price__gte=%s&price__lte=%s' % (new_min, new_min + price_range)
            })
            new_min += price_range + 1

        return prices

    @staticmethod
    def _get_rating_ranges(min_rating, max_rating):
        n_rating_range = max_rating - min_rating
        rating = [
            {
                'key': '%s' % (min_rating + i),
                'value': 'rating__gte=%s' % (min_rating + 1)
            }
            for i in range(n_rating_range)
        ]
        return rating

    @staticmethod
    def _get_discounts(n_discount_ranges=5, **kwargs):
        min_price = kwargs.get('min_price')
        min_discount = kwargs.get('min_discount')
        max_price = kwargs.get('max_price')
        max_discount = kwargs.get('max_discount')

        def to_percentage(discount, price):
            return discount // price * 100

        min_percentage = to_percentage(min_discount, min_price)
        max_percentage = to_percentage(max_discount, min_price)

        discount_range = max_percentage / n_discount_ranges

        discounts = []
        for _ in range(n_discount_ranges):
            discounts.append({
                'key': '%s' % (min_percentage),
                'value': 'discount__gte=%s' % (min_percentage)
            })

            min_percentage += discount_range + 1

        return discounts

    def _filter_mapping(self):
        """
        Product filter keys
        """
        qs = self._product_qs

        brands = qs.values_list('brand', flat=True)
        min_price = qs.aggregate(price=Min('price'))
        max_price = qs.aggregate(price=Max('price'))
        min_rating = qs.aggregate(rating=Min('rating__average_rating'))
        max_rating = qs.aggregate(rating=Max('rating__average_rating'))
        max_discount = qs.aggregate(discount=Max('discount'))
        min_discount = qs.aggregate(discount=Min('discount'))

        min_price = min_price.get('price')
        max_price = max_price.get('price')
        min_rating = min_rating.get('rating')
        max_rating = max_rating.get('rating')
        min_discount = min_discount.get('discount')
        max_discount = max_discount.get('discount')

        discount_args = {
            'min_price': min_price,
            'max_price': max_price,
            'min_discount': min_discount,
            'max_discount': max_discount
        }

        mapping = {
            'brand': [{'key': brand, 'value': 'brand=%s' % (brand)} for brand in brands],
            'price': self._get_price_ranges(min_price, max_price),
            'rating': self._get_rating_ranges(math.floor(min_rating), math.floor(max_rating)),
            'discount': self._get_discounts(**discount_args)
        }

        return mapping

    def _build_filters(self):
        """
        get all product filters including their attributes and filters
        """
        filters = self._filter_mapping()
        attributes = []

        for query in self._product_qs:
            qs_attributes = getattr(query, 'i_attributes', None)

            if qs_attributes:
                for attribute in qs_attributes:
                    attributes.append(attribute.name)
                    variants = []
                    qs_variants = getattr(attribute, 'i_variants', None)

                    if qs_variants:
                        for variant in qs_variants:
                            variants.append({
                                'key': '%s' % (variant.vendor_metric),
                                'value': '%s=%s' % (attribute.name, variant.vendor_metric)
                            })

                    filters[attribute.name] = variants

        self._attributes = attributes
        self._filters = filters

    @property
    def attributes(self):
        """
        Returns Items or products attributes example `color`, `size`
        """
        if not hasattr(self, '_attribute'):
            self._build_filters()

        return self._attributes

    @property
    def filters(self):
        """
        Return a dict containing items or products filters and their respective 
        lookup expressions `{ color: [{ key: 'blue', value: 'color=blue' }] }`
        """
        if not hasattr(self, '_filters'):
            self._build_filters()

        return self._filters
