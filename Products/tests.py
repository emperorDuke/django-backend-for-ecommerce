from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from rest_framework.test import APITestCase
from rest_framework import status

from Stores.models.store import Store
from Products.models.product import Product

from Category.models import Category

from .models.keyFeature import KeyFeature
from .models.specification import Specification
from .models.itemAttribute import Attribute, Variation

from Users.permissions import create_user_permissions


class ProductTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):

        create_user_permissions('seller')

        tree_1 = Category.objects.create(name='fashion')
        child_1 = Category.objects.create(name='men_clothing', parent=tree_1)
        grand_child_1 = Category.objects.create(name='jeans', parent=child_1)

        tree_2 = Category.objects.create(name='electronics')
        child_2 = Category.objects.create(name='note_book', parent=tree_2)
        grand_child_2 = Category.objects.create(name='laptop', parent=child_2)

        cls.category_ref_no = grand_child_1.ref_no

        cls.user_data = {
            'first_name': 'Duke',
            'last_name': 'Effiom',
            'email': 'Effiomduke@gmail.com',
            'password': 'finestduke',
            'phone_number': '+2347037606116',
            "user_type": "seller"
        }

        cls.user = get_user_model().objects.create_user(**cls.user_data)

        cls.store_data = {
            'merchant': cls.user,
            'name': 'Dutex',
            'logo': ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read())
        }

        store = Store.objects.create(**cls.store_data)

        cls.product_data = {
            "attachment_1": open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb'),
            "attachment_2": open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb'),
            "attachment_3": open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb'),
            "attachment_4": open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb'),
            'name': 'samsung galaxy s3',
            'price': 50000.00,
            'discount': 40000.00,
            'category': 'jeans',
            "brand": "Nike",
            'description_text': 'it does this, it does that',
            'description_attachment_1': open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb'),
            'description_attachment_2': open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb'),
            "availability": 'IN STOCK',
            'sku': 'FGR33556'
        }

    def setUp(self):

        token = 'JWT ' + self.user.token

        self.client.credentials(HTTP_AUTHORIZATION=token.encode())

    def test_create(self):

        response = self.client.post('/products/', self.product_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Product.objects.count(), 1)

    def test_update(self):

        self.client.post('/products/', self.product_data)

        product_data = {
            "attachment_1": open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb'),
            "name": "Hisense Tv",
            "discount": '1000.00',
            'category': 'laptop'
        }

        response = self.client.patch('/products/1/', product_data)

        self.assertEqual(response.data['name'], 'Hisense Tv')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['category'], 'laptop')
        self.assertEqual(Product.objects.get(pk=1).name, 'Hisense Tv')

    def test_retrieve(self):

        self.client.post('/products/', self.product_data)

        response = self.client.get('/products/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'samsung galaxy s3')
        self.assertEqual(response.data['category'], 'jeans')
        self.assertEqual(response.data['brand'], 'Nike')

    def test_list(self):

        self.client.post('/products/', self.product_data)

        url = '/products/?category=%s' % (self.category_ref_no)

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'samsung galaxy s3')
        self.assertEqual(response.data[0]['category'], 'jeans')
        self.assertEqual(response.data[0]['brand'], 'Nike')

    def test_delete(self):

        self.client.post('/products/', self.product_data)

        response = self.client.delete('/products/1/')

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(pk=1)

    def test_recently_viewed(self):

        self.client.post('/products/', self.product_data)

        response = self.client.get('/products/recently_viewed/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['category'], 'jeans')
        self.assertEqual(response.data[0]['brand'], 'Nike')

    def test_is_viewed(self):

        self.client.post('/products/', self.product_data)

        response = self.client.post('/products/1/is_viewed/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get(pk=1).viewed.n_views, 1)
    
    def test_listings(self):

        self.client.post('/products/', self.product_data)

        response = self.client.get('/products/listings/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data[0]['latest deals'])


class AttributeTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):

        tree_1 = Category.objects.create(name='fashion')
        child_1 = Category.objects.create(name='men_clothing', parent=tree_1)
        jean_category = Category.objects.create(name='jeans', parent=child_1)

        create_user_permissions('seller')

        cls.user_data = {
            'first_name': 'Duke',
            'last_name': 'Effiom',
            'email': 'Effiomduke@gmail.com',
            'password': 'finestduke',
            'phone_number': '+2347037606116',
            "user_type": "seller"
        }

        cls.user = get_user_model().objects.create_user(**cls.user_data)

        cls.store_data = {
            'merchant': cls.user,
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
            'price': 50000.00,
            'discount': 40000.00,
            'category': jean_category,
            "brand": "Nike",
            'description_text': 'it does this, it does that',
            'description_attachment_1': ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read()),
            'description_attachment_2': ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read()),
            "availability": 'IN STOCK',
            'sku': 'FGR33556'
        }

        cls.product = Product.objects.create(**cls.product_data)

        cls.attributes = {
            'name': 'size',
            'product': cls.product.pk,
            '[variants][0][vendor_metric]': 'XL',
            '[variants][0][metric_verbose_name]': 'Extra large',
            '[variants][0][attachment]': open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb'),
            '[variants][1][vendor_metric]': 'MD',
            '[variants][1][metric_verbose_name]': 'Medium',
            '[variants][1][attachment]': open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb'),
            '[variants][2][vendor_metric]': 'SM',
            '[variants][2][metric_verbose_name]': 'Small',
            '[variants][2][attachment]': open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb'),
        }

        cls.product_meta = {
            'specifications[0][type]': 'weight',
            'specifications[0][value]': '20kg',
            'specifications[0][product]': cls.product.pk,
            'specifications[1][type]': 'product_use',
            'specifications[1][value]': 'multi-use',
            'specifications[1][product]': cls.product.pk,
            'specifications[2][type]': 'warranty',
            'specifications[2][value]': '1 year',
            'specifications[2][product]': cls.product.pk,
            'specifications[3][type]': 'gender',
            'specifications[3][value]': 'male',
            'specifications[3][product]': cls.product.pk,
            'key_features[0][feature]': 'it flys you know',
            'key_features[0][product]': cls.product.pk,
            'key_features[1][feature]': 'it can jump really high',
            'key_features[1][product]': cls.product.pk,
            'key_features[2][feature]': 'you can smoke it',
            'key_features[2][product]': cls.product.pk
        }

    def setUp(self):
        token = 'JWT ' + self.user.token

        self.client.credentials(HTTP_AUTHORIZATION=token.encode())

    def test_create(self):

        response = self.client.post('/products/attributes/', self.attributes)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'size')
        self.assertEqual(Attribute.objects.count(), 1)
        self.assertEqual(Variation.objects.count(), 3)

    def test_update(self):

        self.client.post('/products/attributes/', self.attributes)

        attributes = {
            'id': 1,
            'name': 'colour',
            'product': self.product.pk,
            '[variants][0][id]': 3,
            '[variants][0][attribute]': 1,
            '[variants][0][vendor_metric]': 'XLL',
            '[variants][0][metric_verbose_name]': 'Double extra large',
            '[variants][0][attachment]': open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb'),
            '[variants][1][vendor_metric]': 'XX',
            '[variants][1][metric_verbose_name]': 'Unknown size',
            '[variants][1][attachment]': open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb'),
            '[variants][2][id]': 2,
            '[variants][2][attribute]': 1,
            '[variants][2][vendor_metric]': 'MD',
            '[variants][2][metric_verbose_name]': 'Medium',
            '[variants][2][attachment]': open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb'),
            '[variants][2][delete]': 'true'
        }

        response = self.client.patch('/products/attributes/1/', attributes)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'colour')
        self.assertEqual(Attribute.objects.count(), 1)
        self.assertEqual(Variation.objects.count(), 3)
        self.assertEqual(Variation.objects.get(pk=4).vendor_metric, 'XX')
        with self.assertRaises(Variation.DoesNotExist):
            Variation.objects.get(pk=2)

    def test_retrieve(self):

        self.client.post('/products/attributes/', self.attributes)

        response = self.client.get('/products/1/attributes/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'size')

    def test_create_meta(self):

        response = self.client.post('/products/meta/', self.product_meta)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['specifications'][0]['value'], '20kg')
        self.assertEqual(response.data['key_features']
                         [1]['feature'], 'it can jump really high')
        self.assertEqual(KeyFeature.objects.count(), 3)
        self.assertEqual(Specification.objects.count(), 4)

    def test_update_meta(self):

        self.client.post('/products/meta/', self.product_meta)

        product_meta = {
            'specifications[0][id]': 2,
            'specifications[0][type]': 'cable-length',
            'specifications[0][value]': '5mm',
            'specifications[0][product]': self.product.pk,
            'specifications[1][type]': 'cable-color',
            'specifications[1][value]': 'black',
            'specifications[1][product]': self.product.pk,
            'specifications[2][id]': 3,
            'specifications[2][type]': 'warranty',
            'specifications[2][value]': '1 year',
            'specifications[2][product]': self.product.pk,
            'specifications[2][delete]': 'true',
            'key_features[0][feature]': 'you can cook it',
            'key_features[0][product]': self.product.pk,
            'key_features[1][id]': 3,
            'key_features[1][feature]': 'you can smoke it',
            'key_features[1][product]': self.product.pk,
            'key_features[1][delete]': 'true'
        }

        response = self.client.patch('/products/1/meta/', product_meta)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Specification.objects.count(), 4)
        self.assertEqual(KeyFeature.objects.count(), 3)
        self.assertEqual(Specification.objects.get(pk=2).type, 'cable-length')
        with self.assertRaises(KeyFeature.DoesNotExist):
            KeyFeature.objects.get(pk=3)

    def test_retrieve_meta(self):

        self.client.post('/products/meta/', self.product_meta)

        response = self.client.get('/products/1/meta/s/')

        data = {
            'specifications': [
                {
                    'id': 4,
                    'type': 'gender',
                    'value': 'male',
                    'product': 1
                },
                {
                    'id': 2,
                    'type': 'product_use',
                    'value': 'multi-use',
                    'product': 1
                },
                {
                    'id': 3,
                    'type': 'warranty',
                    'value': '1 year',
                    'product': 1
                },
                {
                    'id': 1,
                    'type': 'weight',
                    'value': '20kg',
                    'product': 1
                }
            ],
            'key_features': [
                {
                    'id': 1,
                    'feature': 'it flys you know',
                    'product': 1
                },
                {
                    'id': 2,
                    'feature': 'it can jump really high',
                    'product': 1
                },
                {
                    'id': 3,
                    'feature': 'you can smoke it',
                    'product': 1
                }
            ]
        }

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, data)
