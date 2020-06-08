from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from rest_framework.test import APITestCase

from Products.models.product import Product
from Category.models import Category

from Stores.models.store import Store

from Users.permissions import create_user_permissions

from .models import StoreReview
from .models import ProductReview
from .models import StoreResponse
from .models import ProductReviewResponse

class ReviewTestCase(APITestCase):

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

        cls.buyer = get_user_model().objects.create_user(**cls.buyer_data)

        cls.product = Product.objects.create(**cls.product_data)

    def setUp(self):

        token = 'JWT ' + self.buyer.token

        self.client.credentials(HTTP_AUTHORIZATION = token.encode())
    
    def test_posting_store_review(self):

        review = {"review":"i love their delivery speed so much"}

        response = self.client.post('/stores/1/review/', review, format='json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['review'], review['review'])

        # testing the list view at once

        response = self.client.get('/stores/1/reviews/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['review'], review['review'])


    def test_multiple_review_from_buyer_to_the_same_store(self):

        review_1 = {
            "review":"i love their delivery speed so much"
        }

        StoreReview.objects.create (
            author=self.buyer,
            store=self.store,
            **review_1
        )

        url = '/stores/1/review/'

        review_2 = {
            "review":"your prices are outrageous"
        }

        response = self.client.post(url, review_2, format='json')

        self.assertNotEqual(response.status_code, 201)
        self.assertEqual(response.data['author'], "multiple reviews from this user on the same store")

    def test_store_response_to_review(self):

        self.client.credentials()

        token = 'JWT ' + self.seller.token

        self.client.credentials(HTTP_AUTHORIZATION = token.encode())

        review = {"review":"your prices are outrageous"}

        StoreReview.objects.create(
            author=self.buyer,
            store=self.store,
            **review
        )

        url = '/stores/review/1/'

        reply_review = {
            "response":"we are ver sorry for the inconvenience, we will do better next time"
        }

        response = self.client.post(url, reply_review, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['response'], reply_review['response'])

        # testing the list view at once
        response = self.client.get('/stores/1/reviews/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['review'], review['review'])
        self.assertEqual(response.data[0]['response']['response'], reply_review['response'])
        
    
    def test_multiple_seller_response_to_store_review(self):

        self.client.credentials()

        token = 'JWT ' + self.seller.token

        self.client.credentials(HTTP_AUTHORIZATION = token.encode())

        review = {
            "review":"your prices are outrageous"
        }

        reply_review = {
            "response":"we are ver sorry for the inconvenience, we will do better next time"
        }

        review_obj = StoreReview.objects.create(
            author=self.buyer,
            store=self.store,
            **review
        )

        review_response = StoreResponse.objects.create (
            review=review_obj,
            author=self.seller,
            **reply_review
        )

        url = '/stores/review/1/'

        reply_review_2 = {
            "response":"we are ver sorry for the inconvenience, we will talk to management"
        }

        response = self.client.post(url, reply_review_2, format='json')

        self.assertNotEqual(response.status_code, 201)
        self.assertEqual(response.data['author'], "number of reply per review is exceeded")

    
    def test_posting_product_review(self):

        url = '/products/1/review/'

        review_1 = {
            "review":"this product taste lovely"
        }

        response = self.client.post(url, review_1, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['review'], review_1['review'])


    def test_multiple_review_from_buyer(self):

        review_1 = {
            "review":"i love their delivery speed so much"
        }

        ProductReview.objects.create (
            author=self.buyer,
            product=self.product,
            **review_1
        )

        url = '/products/1/review/'

        review_2 = {
            "review":"your prices are outrageous"
        }

        response = self.client.post(url, review_2, format='json')

        self.assertNotEqual(response.status_code, 201)
        self.assertEqual(response.data['author'], "multiple reviews from this user on the same product")

    def test_store_response_to_product_review(self):

        self.client.credentials()

        token = 'JWT ' + self.seller.token

        self.client.credentials(HTTP_AUTHORIZATION = token.encode())

        review = {
            "review":"your prices are outrageous"
        }

        review = ProductReview.objects.create(
            author=self.buyer,
            product=self.product,
            **review
        )

        url = '/products/review/1/'

        reply_review = {
            "response":"we are ver sorry for the inconvenience, we will do better next time"
        }

        response = self.client.post(url, reply_review, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['response'], reply_review['response'])
    
    def test_multiple_seller_response(self):

        self.client.credentials()

        token = 'JWT ' + self.seller.token

        self.client.credentials(HTTP_AUTHORIZATION = token.encode())

        review = {
            "review":"your prices are outrageous"
        }

        reply_review = {
            "response":"we are ver sorry for the inconvenience, we will do better next time"
        }

        review_obj = ProductReview.objects.create(
            author=self.buyer,
            product=self.product,
            **review
        )

        review_response = ProductReviewResponse.objects.create (
            review=review_obj,
            author=self.seller,
            **reply_review
        )

        url = '/products/review/1/'

        reply_review_2 = {
            "response":"we are ver sorry for the inconvenience, we will talk to management"
        }

        response = self.client.post(url, reply_review_2, format='json')
        print(response.data)

        self.assertNotEqual(response.status_code, 201)
        self.assertEqual(response.data['non_field_error'], "number of reply per review is exceeded")

    def test_list_of_product_reviews(self):

        review = {
            "review":"your prices are outrageous"
        }

        reply_review = {
            "response":"we are ver sorry for the inconvenience, we will do better next time"
        }

        review_obj = ProductReview.objects.create(
            author=self.buyer,
            product=self.product,
            **review
        )

        review_response = ProductReviewResponse.objects.create (
            review=review_obj,
            author=self.seller,
            **reply_review
        )

        response = self.client.get('/products/1/reviews/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['review'], review['review'])
        self.assertEqual(response.data[0]['response']['response'], reply_review['response'])
















# Create your tests here.
