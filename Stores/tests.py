from django.contrib.auth import get_user_model

from rest_framework.test import APITestCase
from rest_framework import status

from .models.store import Store

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
            '[address][street_address]': 'no 34 beckham street, ikeja Lagos',
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

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['address']['default'])
        self.assertEqual(response.data['name'], 'Dutex')

    def test_retrieve_store(self):

        self.client.post('/stores/', self.store_data)

        response = self.client.get('/stores/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_store(self):

        self.client.post('/stores/', self.store_data)

        store_data = {
            '[address][id]': 1,
            '[address][user]': 1,
            '[address][street_address]': 'no 15 adeshina street olugbede market',
            '[address][zip_code]': '98778787',
            '[address][country]': 'Nigeria'
        }

        response = self.client.patch('/stores/1/', store_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Dutex')
        self.assertEqual(
            response.data['address']['street_address'], store_data['[address][street_address]'])

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
