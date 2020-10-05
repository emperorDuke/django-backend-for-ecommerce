from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from .permissions import create_user_permissions


class UserTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):

        create_user_permissions('seller')
        create_user_permissions('buyer')

        cls.data = {
            'first_name': 'Duke',
            'last_name': 'Effiom',
            'email': 'Effiomduke@gmail.com',
            'password': 'finestduke',
            'phone_number': '+2347037606116',
        }

        cls.buyer_data = {
            'first_name': 'Duke',
            'middle_name': 'Damola',
            'last_name': 'Effiom',
            'email': 'Effiomduke@gmail.com',
            'password': 'finestduke',
            'phone_number': '+2347037606116',
        }

        cls.address = {
            '[address][address]': 'no 34 beckham street, ikeja Lagos',
            '[address][country]': 'Nigeria',
            '[address][city]': 'Ikeja',
            '[address][state]': 'Lagos',
            '[address][zip_code]': '35467',
        }

        cls.buyer_data

    def test_create_seller(self):

        url = '/seller/users/'

        response = self.client.post(url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_create_buyer(self):

        url = '/buyer/users/'

        response = self.client.post(url, self.buyer_data, format='json')

        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.count(), 1)

    def test_user(self):

        data = {
            'email': 'Effiomduke@gmail.com',
            'password': 'finestduke'
        }

        user = get_user_model().objects.create_user(**self.data)
        user.is_active = True
        user.save()

        response = self.client.post('/seller/users/login/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['token'])

        ########################################################################

        token = 'JWT ' + response.data['token']

        self.client.credentials(HTTP_AUTHORIZATION=token.encode())

        data = {
            'first_name': 'John',
            'middle_name': 'olamide'
        }

        response = self.client.patch('/seller/users/1/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['middle_name'], 'olamide')

        ######################################################################

        response = self.client.get('/seller/users/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')
