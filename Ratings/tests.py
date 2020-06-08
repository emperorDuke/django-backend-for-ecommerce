from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from rest_framework.test import APITestCase

from Users.permissions import create_user_permissions

from Products.models.product import Product
from Category.models import Category

from Stores.models.store import Store


class RatingTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):

        create_user_permissions('seller')

        create_user_permissions('buyer')

        cls.seller_data = {
            'first_name': 'Duke',
            'last_name': 'Effiom',
            'email': 'bbruise@gmail.com',
            'password': 'finestduke',
            'phone_number': '+2347037606116',
            'user_type': 'seller' 
        }

        cls.buyer_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'effiomduke@gmail.com',
            'password': 'finestduke',
            'phone_number': '+2347037606118',
            'user_type': 'buyer'
        }

        cls.seller = get_user_model().objects.create_user(**cls.seller_data)

        cls.store_data = {
            'merchant': cls.seller,     
            'name':'Dutex',
            'logo': ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read())
        }

        cls.store = Store.objects.create(**cls.store_data)

        tree_1 = Category.objects.create(name='fashion')
        child_1 = Category.objects.create(name='men_clothing', parent=tree_1)
        jean_category = Category.objects.create(name='jeans', parent=child_1)
        
        cls.product_data = {
            'store': cls.store,
            "attachment_1": ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read()),
            "attachment_2": ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read()),
            "attachment_3": ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read()),
            "attachment_4": ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read()),
            'name' :'samsung galaxy s3',
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

        buyer = get_user_model().objects.create_user(**cls.buyer_data)

        cls.token = 'JWT ' + buyer.token

        
    def setUp(self):

        self.client.credentials(HTTP_AUTHORIZATION = self.token.encode())


    def test_store_rating(self):

        url = '/stores/1/rating/'

        response = self.client.patch(url, {'n_stars': 2}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['average_rating'], '2.0')

    def test_product_rating(self):

        url = '/products/1/rating/'

        self.client.patch(url, {'n_stars': 3}, format='json')

        self.client.patch(url, {'n_stars': 2}, format='json')

        self.client.patch(url, {'n_stars': 5}, format='json')

        response = self.client.patch(url, {'n_stars': 5}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['average_rating'], '4.0')
