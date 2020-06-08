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

from Location.models import Location

from Category.models import Category

from Cart.models.cart import Cart

from .models import orders, ordered_item


class OrderTestCase(APITestCase):

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

        cls.buyer_profile = BuyerProfile.objects.get(user=cls.buyer)

        cart_items = [
            {
                'buyer': cls.buyer_profile,
                'product': cls.product,
                'quantity': 2,
                'price': '5000.00',
            }
        ]

        cart = [
            Cart.objects.create(**item)
            for item in cart_items
        ]

        for item in cart:
            item.variants.set(attribute_variants)

        cls.address = {
            'address': 'no 34 beckham street, ikeja Lagos',
            'country': 'Nigeria',
            'city': 'Ikeja',
            'state': 'Lagos',
            'zip_code': '35467',
        }

        address_obj = Address.objects.create(**cls.address)

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

        location_data = [
            {
                'address': 'no 34 beckham street, ikeja Lagos',
                'country': 'Nigeria',
                'city': 'Ikeja',
                'state': 'Lagos',
                'zip_code': '35467'
            }
        ]

        cls.location_obj = Location.objects.create(**location_data[0])

        cls.token = 'JWT ' + cls.buyer.token

    def setUp(self):

        self.client.credentials(HTTP_AUTHORIZATION=self.token.encode())

    def test_create_order(self):

        response = self.client.post('/order/')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(ordered_item.OrderedItem.objects.count(), 1)
        self.assertEqual(orders.Order.objects.count(), 1)
        self.assertEqual(ordered_item.OrderedItem.objects.get(
            pk=1).name, 'samsung galaxy s3')
        self.assertEqual(ShippingDetail.objects.get(pk=1).default, True)

    def test_update(self):
        """
        shipping_details can be updated or created from order
        """

        self.client.post('/order/')

        order = {
            'id': 1,
            'delivery_method': orders.Order.PUS,
            'payment_method': orders.Order.PAYNOW,
            '[pickup_site][address]':'no 34 beckham street, ikeja Lagos',
            '[pickup_site][country]': 'Nigeria',
            '[pickup_site][state]': 'Lagos',
            '[pickup_site][city]': 'Ikeja',
            '[pickup_site][id]': 1,
            '[shipping_detail][id]': 1,
            '[shipping_detail][first_name]': 'Duncan',
            '[shipping_detail][last_name]': 'Effiom',
            '[shipping_detail][phone_number]': '+2347037606116',
            '[shipping_detail][default]': False,
            '[shipping_detail][address][id]': 1,
            '[shipping_detail][address][address]': 'block 8 plot 13 federal housing',
            '[shipping_detail][address][city]': 'Calabar municipality',
            '[shipping_detail][address][country]': 'Nigeria',
            '[shipping_detail][address][state]': 'Calabar'
        }
        response = self.client.patch('/order/1/', order)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['shipping_detail']['default'], False)
        self.assertEqual(response.data['shipping_detail']['first_name'], 'Duncan')

    def test_list(self):
        self.client.post('/order/')
        response = self.client.get('/order/')

        self.assertEqual(response.status_code, 200)