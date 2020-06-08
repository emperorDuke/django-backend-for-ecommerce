from rest_framework import serializers

from ..models.itemAttribute import Attribute, Variation


class VariationListSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        ret = []

        for variant in validated_data:
            variant['attribute'] = self.context['attribute']
            ret.append(Variation(**variant))

        return Variation.objects.bulk_create(ret)

    def update(self, instance, validated_data):
        data_for_deletion = []

        for i, data in enumerate(validated_data):
            if 'delete' in data and data['delete']:
                data_for_deletion.append(validated_data.pop(i))

        data_mapping = {item.get('id', None): item for item in validated_data}
        variant_mapping = {variant.id: variant for variant in instance}

        ret = []

        # creation and updating operation #

        for variant_id, data in data_mapping.items():
            variant = variant_mapping.get(variant_id, None)
            if variant is None:
                data['attribute'] = self.context['attribute']
                ret.append(self.child.create(data))
            else:
                del data['id']
                ret.append(self.child.update(variant, data))

        # deletion operation #

        for data in data_for_deletion:
            instance = variant_mapping.get(data.get('id'))
            instance.delete()

        return ret


class VariationSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    delete = serializers.BooleanField(required=False)

    class Meta:
        model = Variation
        list_serializer_class = VariationListSerializer
        validators = []
        fields = '__all__'
        read_only_fields = ('attribute',)

    def to_representation(self, instance):
        if 'delete' in self.fields:
            self.fields.pop('delete')

        return super().to_representation(instance)


class AttributeSerializer(serializers.ModelSerializer):

    variants = VariationSerializer(many=True)

    class Meta:
        model = Attribute
        validators = []
        fields = (
            'id',
            'variants',
            'name',
            'product'
        )

    def get_variants_serializer(self):
        return self.fields.get('variants', None)

    def create(self, validated_data):
        product = validated_data.get('product', None)
        name = validated_data.get('name', None)
        variants = validated_data.get('variants', [])

        attribute = Attribute.objects.create(name=name, product=product)

        if variants:
            if len(variants) > 1:
                serializer = self.get_variants_serializer()
                serializer.context['attribute'] = attribute
                serializer.create(variants)
            elif len(variants) == 1:
                variants[0]['attribute'] = attribute
                Variation.objects.create(**variants[0])

        return attribute

    def update(self, instance, validated_data):

        variants_data = validated_data.pop('variants', None)
        variants_instance = getattr(instance, 'i_variants', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)
            instance.save()

        if variants_instance and variants_data:
            serializer = self.get_variants_serializer()
            serializer.context['attribute'] = instance
            serializer.update(variants_instance, variants_data)

        return instance
