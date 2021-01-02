from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from rest_framework.test import APITestCase

from Users.permissions import create_user_permissions
from Users.models.address import Address

from Stores.models import Store

from Products.models.itemAttribute import Variation, Attribute
from Products.models.product import Product

from Buyer.models.profile import Profile

from Category.models import Category

from Cart.models.cart import Cart

from .models import Coupon


class PaymentTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):

        create_user_permissions('buyer')

        create_user_permissions('seller')

        cls.buyer_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'effiomduke@gmail.com',
            'password': 'finestduke',
            'phone_number': '+2347037606118',
            'user_type': 'buyer'
        }

        tree_1 = Category.objects.create(name='fashion')
        child_1 = Category.objects.create(name='men_clothing', parent=tree_1)
        jean_category = Category.objects.create(name='jeans', parent=child_1)

        cls.seller_data = {
            'first_name': 'Duke',
            'last_name': 'Effiom',
            'email': 'Effiomduke@gmail.com',
            'password': 'finestduke',
            'phone_number': '+2347037606116',
            "user_type": "seller"
        }

        cls.seller = get_user_model().objects.create_user(**cls.seller_data)

        cls.store_data = {
            'merchant': cls.seller,
            'name': 'Dutex',
            'logo': ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read())
        }

        store = Store.objects.create(**cls.store_data)

        cls.product_data = {
            'store': store,
            "attachment_1": ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read()),
            "attachment_2": ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read()),
            "attachment_3": ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read()),
            "attachment_4": ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read()),
            'name': 'samsung galaxy s3',
            'price': '50000.00',
            'discount': '40000.00',
            'category': jean_category,
            "brand": "Nike",
            'description_text': 'it does this, it does that',
            'description_attachment_1': ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read()),
            'description_attachment_2': ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read()),
            "availability": 'IN STOCK',
            'sku': 'FGR33556'
        }

        cls.product = Product.objects.create(**cls.product_data)

        product_attribute = {
            'product': cls.product,
            'name': 'size'
        }

        attribute = Attribute.objects.create(**product_attribute)

        variations = [
            {
                'attribute': attribute,
                'vendor_metric': 'L',
                'metric_verbose_name': 'Large',
                'attachment': ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read())
            },
            {
                'attribute': attribute,
                'vendor_metric': 'S',
                'metric_verbose_name': 'Small',
                'attachment': ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read())
            },
            {
                'attribute': attribute,
                'vendor_metric': 'XL',
                'metric_verbose_name': 'extra large',
                'attachment': ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read())
            }
        ]

        attribute_variants = [
            Variation.objects.create(**variant)
            for variant in variations
        ]

        cls.buyer = get_user_model().objects.create_user(**cls.buyer_data)

        cls.buyer_profile = Profile.objects.get(user=cls.buyer)

        cart_items = [
            {
                'buyer': cls.buyer_profile,
                'product': cls.product,
                'quantity': 2,
                'price': '5000',
            }
        ]

        cart = [
            Cart.objects.create(**item)
            for item in cart_items
        ]

        for item in cart:
            item.variants.set(attribute_variants)

        cls.address = {
            'user': cls.buyer,
            'street_address': 'no 34 beckham street, ikeja Lagos',
            'country': 'Nigeria',
            'city': 'Lagos',
            'zip_code': '35467',
            'default': True
        }

        cls.coupon_code = '45kk67'

        Address.objects.create(**cls.address)

        Coupon.objects.create(code=cls.coupon_code, amount=350.00)

        cls.token = 'JWT ' + cls.buyer.token

    def setUp(self):

        self.client.credentials(HTTP_AUTHORIZATION=self.token.encode())

    def test_post_coupon(self):

        self.client.post('/order/')

        response = self.client.post('/order/1/coupon/', {'code': self.coupon_code}, format='json')

        self.assertEqual(response.status_code, 200)


