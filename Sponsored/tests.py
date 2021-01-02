from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from rest_framework.test import APITestCase

from Users.permissions import create_user_permissions
from Users.models.address import Address

from Category.models import Category
from Stores.models.store import Store
from Products.models.itemAttribute import Variation, Attribute
from Products.models.product import Product

from Sponsored.models import SponsoredProduct, SponsoredStore

from .models import AdsPlan


# Create your tests here.

class SponsoredTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):

        create_user_permissions('seller')

        tree_1 = Category.objects.create(name='fashion')
        child_1 = Category.objects.create(name='men_clothing', parent=tree_1)
        jean_category = Category.objects.create(name='jeans', parent=child_1)

        cls.seller_data = {
            'first_name': 'Duke',
            'last_name': 'Effiom',
            'email': 'Effiomduke@gmail.com',
            'password': 'finestduke',
            'phone_number': '+2347037606116',
            "user_type": "SELLER"
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

        cls.ads_plan_obj = AdsPlan.objects.create(
            name='one week',
            amount=5000.00,
            duration=5,
        )

        cls.token = 'JWT ' + cls.seller.token

    def setUp(self):

        self.client.credentials(HTTP_AUTHORIZATION=self.token.encode())

    def test_create_sponsored_product(self):

        data = {
            'item_id': 1,
            'ads_plan': self.ads_plan_obj.pk
        }

        expected_data = {
            'product': {
                'id': 1, 
                'store': 1, 
                'name': 'samsung galaxy s3', 
                'price': '50000.00', 
                'discount': '40000.00', 
                'brand': 'Nike', 
                'category': 'jeans', 
                'sku': 'FGR33556', 
                'availability': 'IN STOCK', 
                'attachment_1': None, 
                'attachment_2': None, 
                'attachment_3': None, 
                'attachment_4': None, 
                'rating': {
                    'average_rating': '0.0', 
                    'n_one_star_votes': 0, 
                    'n_two_stars_votes': 0, 
                    'n_three_stars_votes': 0, 
                    'n_four_stars_votes': 0, 
                    'n_five_stars_votes': 0, 
                    'n_votes': 0
                    }, 
                'description_text': 'it does this, it does that', 
                'description_attachment_1': None, 
                'description_attachment_2': None, 
                'ref_no': '329230'
                }, 
            'payment': {
                'id': 1, 
                'ref_no': '329288', 
                'amount': 5000.0, 
                'status': 'not paid', 
                'created_at': '2020-06-20T13:00:08.118980Z', 
                'user': 1
            }, 
            'plan': {
                'id': 1, 
                'name': 'one week', 
                'amount': 5000.0, 
                'duration': 5, 
                'added_at': '2020-06-20T13:00:08.074050Z', 
                'ref_no': '329253'
            }, 
            'has_expired': False, 
            'start_at': '2020-06-20T13:00:08.121975Z', 
            'ref_no': '329293', 
            'status': 'PROCESSING'
            }

        response = self.client.post('/sponsored/products/', data, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(SponsoredProduct.objects.count(), 1)

    
    def test_create_sponsored_store(self):
        data = {
            'item_id': 1,
            'ads_plan': self.ads_plan_obj.pk
        }

        response = self.client.post('/sponsored/stores/', data, formate='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(SponsoredStore.objects.count(), 1)


    def update_sponsored_product(self):
        data = {
            'item_id': 1,
            'ads_plan': self.ads_plan_obj.pk
        }

        self.client.post('/sponsored/products/', data, format='json')

        next_data = {
            'start_sub': True
        }

        response = self.client.patch('/sponsored/products/1/', next_data, format='json')

        self.assertEqual(response.status_code, 200)

    def update_sponsored_store(self):

        data = {
            'item_id': 1,
            'ads_plan': self.ads_plan_obj.pk
        }

        self.client.post('/sponsored/stores/', data, format='json')

        next_data = {
            'start_sub': True
        }

        response = self.client.patch('/sponsored/stores/1/', next_data, format='json')

        self.assertEqual(response.status_code, 200)


