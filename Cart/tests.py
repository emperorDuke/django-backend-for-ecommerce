from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from rest_framework.test import APITestCase

from Users.permissions import create_user_permissions
from Users.models.address import Address

from Stores.models import Store

from Products.models.itemAttribute import Variation, Attribute
from Products.models.product import Product

from BuyerProfile.models.profile import BuyerProfile
from BuyerProfile.models.shipping_detail import ShippingDetail

from Category.models import Category

from .models.cart import Cart


class CartTestCase(APITestCase):

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

        cls.attribute = Attribute.objects.create(**product_attribute)

        variations = [
            {
                'attribute': cls.attribute,
                'vendor_metric': 'L',
                'metric_verbose_name': 'Large',
                'attachment': ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read())
            },
            {
                'attribute': cls.attribute,
                'vendor_metric': 'S',
                'metric_verbose_name': 'Small',
                'attachment': ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read())
            },
            {
                'attribute': cls.attribute,
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

        cls.buyer_profile = BuyerProfile.objects.get(user=cls.buyer)

        address = {
            'address': 'no 34 beckham street, ikeja Lagos',
            'country': 'Nigeria',
            'city': 'Ikeja',
            'state':'Lagos',
            'zip_code': '35467',
        }

        address_obj = Address.objects.create(**address)

        cls.shipping_detail = {
            'buyer': cls.buyer_profile,
            'first_name': cls.buyer.first_name,
            'middle_name': cls.buyer.middle_name,
            'last_name': cls.buyer.last_name,
            'phone_number': cls.buyer.phone_number,
            'address': address_obj,
            'default': True
        }

        ShippingDetail.objects.create(**cls.shipping_detail)

        cls.cart = {
            'product': cls.product.pk,
            'quantity': 2,
            'price': '5000',
            'variants[0][id]': 1,
            'variants[0][attribute]': 1,
            'variants[0][vendor_metric]': 'L',
            'variants[0][metric_verbose_name]': 'Large'
        }

        cls.token = 'JWT ' + cls.buyer.token

    def setUp(self):

        self.client.credentials(HTTP_AUTHORIZATION = self.token.encode())

    def test_create(self):

        response = self.client.post('/cart/', self.cart, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Cart.objects.count(), 1)
        # self.assertEqual(response.data['product']['name'], 'samsung galaxy s3')

    def test_update(self):

        self.client.post('/cart/', self.cart, format='json')

        cart = {
            'id': 1,
            'buyer': 1,
            'product': self.product.pk,
            'quantity': 10,
            'price': '8000',
            'variants[0][id]': 1,
            'variants[0][attribute]': 1,
            'variants[0][vendor_metric]': 'L',
            'variants[0][metric_verbose_name]': 'Large',
            'variants[1][id]': 2,
            'variants[1][attribute]': 1,
            'variants[1][vendor_metric]': 'S',
            'variants[1][metric_verbose_name]': 'Small',
        }

        response = self.client.patch('/cart/1/', cart, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cart.objects.get(pk=1).variants.count(), 2)
        self.assertEqual(response.data['price'], '8000.00')

    def test_list(self):

        self.client.post('/cart/', self.cart, format='json')

        response = self.client.get('/cart/', format='json')
  
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['variants'][0]['vendor_metric'], 'L')

    def test_delete(self):
        self.client.post('/cart/', self.cart, format='json')

        response = self.client.delete('/cart/1/')

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Cart.DoesNotExist):
            Cart.objects.get(pk=1)
