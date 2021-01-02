from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from rest_framework.test import APITestCase
from rest_framework import status

from .models.store import Store
from .models.advert import Advert

from Users.permissions import create_user_permissions


class StoreTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):

        create_user_permissions('seller')

        cls.user_data = {
            'first_name': 'Duke',
            'last_name': 'Effiom',
            'email': 'Effiomduke@gmail.com',
            'password': 'finestduke',
            'phone_number': '+2347037606116',
            'user_type': 'seller'
        }

        cls.store_data = {
            'name': 'Dutex',
            '[address][address]': 'no 34 beckham street, ikeja Lagos',
            '[address][country]': 'Nigeria',
            '[address][city]': 'Ikeja',
            '[address][state]': 'Lagos',
            '[address][zip_code]': '35467',
            'logo': open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb'),
        }

        user = get_user_model().objects.create_user(**cls.user_data)

        token = 'JWT ' + user.token

        cls.b_token = token.encode()

    def setUp(self):

        self.client.credentials(HTTP_AUTHORIZATION=self.b_token)

    def test_post_store(self):

        response = self.client.post('/stores/', self.store_data)

        expected_data = {
            'id': 1, 
            'merchant': 1, 
            'logo': 'http://testserver/media/uploads/Dutex/logo/hp_42ee85b5f3ac14b5367b2a998a8bcabc_0Blrr8p.jpg', 
            'name': 'Dutex', 
            'rating': {
                'average_rating': '0.0', 
                'n_one_star_votes': 0, 
                'n_two_stars_votes': 0, 
                'n_three_stars_votes': 0, 
                'n_four_stars_votes': 0, 
                'n_five_stars_votes': 0, 
                'n_votes': 0
            }, 
            'address': {
                'id': 1, 
                'address': 'no 34 beckham street, ikeja Lagos', 
                'city': 'Ikeja', 
                'country': 'Nigeria', 
                'zip_code': '35467', 
                'state': 'Lagos', 
                'added_at': '2020-09-29'
                }, 
            'ref_no': '172884'
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['rating'], expected_data['rating'])
        self.assertEqual(response.data['address'], expected_data['address'])
        self.assertEqual(response.data['name'], expected_data['name'])

    def test_retrieve_store(self):

        self.client.post('/stores/', self.store_data)

        response = self.client.get('/stores/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_store(self):

        self.client.post('/stores/', self.store_data)

        store_data = {
            '[address][id]': 1,
            '[address][user]': 1,
            '[address][address]': 'no 15 adeshina street olugbede market',
            '[address][zip_code]': '98778787',
            '[address][country]': 'Nigeria'
        }

        response = self.client.patch('/stores/1/', store_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Dutex')
        self.assertEqual(
            response.data['address']['address'], store_data['[address][address]'])

    def test_list_store(self):

        self.client.post('/stores/', self.store_data)

        response = self.client.get('/store/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Dutex')

    def test_delete_store(self):

        self.client.post('/stores/', self.store_data)

        response = self.client.delete('/store/1/')

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Store.DoesNotExist):
            Store.objects.get(pk=1)

    def test_store_locations(self):

        self.client.post('/stores/', self.store_data)

        response = self.client.get('/stores/locations/')

        self.assertEqual(response.data[0], 'Lagos')
        self.assertEqual(response.status_code, 200)


class AdvertTestCase(APITestCase):

    bearer = "JWT"

    @classmethod
    def setUpTestData(cls):

        create_user_permissions('seller')

        cls.user_data = {
            'first_name': 'Duke',
            'last_name': 'Effiom',
            'email': 'bbruise@gmail.com',
            'password': 'finestduke',
            'phone_number': '+2347037606116',
            'user_type': 'seller'
        }

        cls.seller = get_user_model().objects.create_user(**cls.user_data)

        cls.store_data = {
            'merchant': cls.seller,
            'name': 'Dutex',
            'logo': ContentFile(open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb').read()),
        }

        cls.store = Store.objects.create(**cls.store_data)

        cls.adverts = {
            'store': cls.store.pk,
            'attachment': open('C:/Users/DUKE/Pictures/Saved Pictures/hp_42ee85b5f3ac14b5367b2a998a8bcabc.jpg', 'rb'),
            'text': 'we will be having a monthly sale at the eko hotel and suites this friday'
        }

    def setUp(self):

        token = self.bearer + " " + self.seller.token

        self.client.credentials(HTTP_AUTHORIZATION=token.encode())

    def test_create(self):
        response = self.client.post('/adverts/', self.adverts)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Advert.objects.count(), 1)

    def test_update(self):
        self.client.post('/adverts/', self.adverts)

        advert = {
            'store': self.store.pk,
            'attachment': open('C:/Users/DUKE/Pictures/Saved Pictures/bjuububuubbu.jpg', 'rb'),
            'text': 'we will be having a monthly sale at the eko hotel and suites this tuesday'
        }

        response = self.client.patch('/adverts/1/', advert)

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(
            response.data['text'],
            'we will be having a monthly sale at the eko hotel and suites this friday'
        )

    def test_list(self):
        self.client.post('/adverts/', self.adverts)

        response = self.client.get('/adverts/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data[0]['text'],
            'we will be having a monthly sale at the eko hotel and suites this friday'
        )

    def test_retrieve(self):

        self.client.post('/adverts/', self.adverts)

        response = self.client.get('/adverts/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['text'],
            'we will be having a monthly sale at the eko hotel and suites this friday'
        )

    def test_delete(self):
        self.client.post('/adverts/', self.adverts)

        response = self.client.delete('/adverts/1/')

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Advert.DoesNotExist):
            Advert.objects.get(pk=1)
