from rest_framework import filters


class AttributeFilter(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):

        for key, value in request.query_params.items():

            queryset = queryset.filter(attribute__name=key).filter(
                attribute__variation__vendor_metric=value)

        return queryset


class ProductFilter(filters.BaseFilterBackend):

    def filter_queryset(self, queryset, request, view):

        for key, value in request.query_params.items():
            queryset = queryset.filter(**{key: value})

        return queryset
