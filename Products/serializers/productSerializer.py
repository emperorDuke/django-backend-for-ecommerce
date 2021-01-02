from rest_framework import serializers

from Ratings.serializers.productRatingSerializer import ProductRatingSerializer

from ..models.product import Product

from .itemAttributeSerializer import AttributeSerializer

from Category.models import Category


class ProductSerializer(serializers.ModelSerializer):

    rating = ProductRatingSerializer(read_only=True)
    category = serializers.CharField()
    store = serializers.PrimaryKeyRelatedField(read_only=True)
    ref_no = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'store',
            'name',
            'price',
            'discount',
            'brand',
            'category',
            'sku_no',
            'availability',
            'attachment_1',
            'attachment_2',
            'attachment_3',
            'attachment_4',
            'rating',
            'description_text',
            'description_attachment_1',
            'description_attachment_2',
            'ref_no'
        )

    @staticmethod
    def set_category(validated_data):

        if 'category' in validated_data:
            category_data = validated_data.pop('category')
            category_instance = Category.objects.get(name=category_data)
            return category_instance

        return None

    def create(self, validated_data):
        category_instance = self.set_category(validated_data)

        if category_instance:
            validated_data['category'] = category_instance

        store_instance = self.context['request'].user.store

        validated_data['store'] = store_instance

        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        category_instance = self.set_category(validated_data)

        if category_instance:
            validated_data['category'] = category_instance

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
