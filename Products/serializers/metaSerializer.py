from django.shortcuts import get_object_or_404

from rest_framework import serializers

from ..models.product import Product

from .keyFeatureSerializer import KeyFeatureSerializer
from .specificationSerializer import SpecificationSerializer


SPECIFICATIONS = 'specifications'
FEATURES = 'key_features'


def get_instance(pk=None):
    product = get_object_or_404(Product, pk=pk)
    return {
        SPECIFICATIONS: product.specifications.all(),
        FEATURES: product.key_features.all()
    }


class MetaSerializer(serializers.Serializer):

    specifications = SpecificationSerializer(many=True)
    key_features = KeyFeatureSerializer(many=True)

    def create(self, validated_data):
        features_field = self.fields.get(FEATURES, None)
        specs_field = self.fields.get(SPECIFICATIONS, None)
        ret = {}

        specs_data = validated_data.get(SPECIFICATIONS, None)
        features_data = validated_data.get(FEATURES, None)

        if specs_field and specs_data:
            specs_list = specs_field.create(specs_data)
            ret[SPECIFICATIONS] = specs_list

        if features_field and features_data:
            features_list = features_field.create(features_data)
            ret[FEATURES] = features_list

        return ret

    def update(self, instance, validated_data):
        features_field = self.fields.get(FEATURES, None)
        specs_field = self.fields.get(SPECIFICATIONS, None)
        ret = {}

        specs_data = validated_data.get(SPECIFICATIONS, None)
        features_data = validated_data.get(FEATURES, None)

        if specs_field and specs_data:
            obj = instance.get(SPECIFICATIONS, None)
            specs_list = specs_field.update(obj, specs_data)
            ret[SPECIFICATIONS] = specs_list

        if features_field and features_data:
            obj = instance.get(FEATURES, None)
            features_list = features_field.update(obj, features_data)
            ret[FEATURES] = features_list

        return ret

    def to_representation(self, instance):
        features_field = self.fields.get(FEATURES, None)
        specs_field = self.fields.get(SPECIFICATIONS, None)
        ret = {}

        specs_instance = instance.get(SPECIFICATIONS, None)
        features_instance = instance.get(FEATURES, None)

        if specs_field and specs_instance:
            ret_specs = specs_field.to_representation(specs_instance)
            ret[SPECIFICATIONS] = ret_specs

        if features_field and features_instance:
            ret_features = features_field.to_representation(features_instance)
            ret[FEATURES] = ret_features

        return ret
