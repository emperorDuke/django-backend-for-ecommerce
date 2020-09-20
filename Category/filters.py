from functools import reduce

from rest_framework import filters

from .models import Category


class CategoryFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        
        query_param = request.query_params.get('category', None)
        instance = Category.objects.get(ref_no=query_param)
        queries = []

        if instance.is_root_node():
            node_descendants = instance.get_descendants()
            for qs in node_descendants:
                if qs.is_child_node() and qs.is_leaf_node():
                    queries.append(queryset.filter(category=qs))
        else:
            queries.append(queryset.filter(category=instance))

        return reduce(lambda x, y: x.union(y), queries)

        