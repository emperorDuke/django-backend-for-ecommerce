from django.shortcuts import get_object_or_404

from rest_framework import serializers

from ..models.productReviews import ProductReview

from .productReviewResponseSerializer import ProductReviewResSerializer

from Products.models.product import Product


class ProductReviewSerializer(serializers.ModelSerializer):

    response = ProductReviewResSerializer(read_only=True)
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)


    class Meta:
        model = ProductReview
        fields =  ('id','author','product', 'response','review')
        validators = []

    
    def get_product(self, obj=None):
        productPk = self.context['view'].kwargs.get('productPk')
        product = get_object_or_404(Product, pk=productPk)
        return product

    def get_author(self, obj=None):
        return self.context['request'].user

    def to_internal_value(self, data):
        review_sets = self.get_product().reviews

        if review_sets.filter(author=self.get_author()).exists():
            raise serializers.ValidationError({
                "author" : "multiple reviews from this user on the same product"
                })
        
        return super().to_internal_value(data)


    def create(self, validated_data):
        author = self.get_author()
        product = self.get_product()

        return ProductReview.objects.create(
            author=author,
            product=product,
            **validated_data
        )
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['author'] = instance.author.get_short_name
        return ret