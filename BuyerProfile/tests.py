from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from Users.permissions import create_user_permissions

from Users.models.address import Address
from .models.shipping_detail import ShippingDetail

# Create your tests here.
##################################################################
##                    #####   #####                             ##
##                         ##                                   ##
##                       ######                                 ##
##                                                              ##
##################################################################

class ShippingDetailTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        create_user_permissions('buyer')

        cls.user_data = {
            'first_name': 'Duke',
            'last_name': 'Effiom',
            'email': 'Effiomduke@gmail.com',
            'password': 'finestduke',
            'phone_number': '+2347037606116',
            'user_type': 'buyer'
        }

        cls.user = get_user_model().objects.create_user(**cls.user_data)

        token = 'JWT ' + cls.user.token

        cls.b_token = token.encode()

        cls.main_address = {
            'user': cls.user,
            'street_address': 'no 34 beckham street, ikeja Lagos',
            'country': 'Nigeria',
            'city': 'Lagos',
            'zip_code': '35467',
        }

        Address.objects.create(**cls.main_address)

    def setUp(self):

        self.client.credentials(HTTP_AUTHORIZATION=self.b_token)

    def test_update(self):

        address = {
            'street_address': 'no 34 beckham street, ikeja Abuja',
            'city': 'Abuja',
        }

        response = self.client.patch('/address/1/', address, format='json')
        

        self.assertEqual(response.status_code, 200)

    def test_list(self):

        main_address = {
            'user': self.user,
            'street_address': 'no 2 olugbede street idumu, lagos',
            'country': 'Nigeria',
            'city': 'Lagos',
            'zip_code': '35464',
        }

        Address.objects.create(**main_address)

        response = self.client.get('/address/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data[1]['street_address'], main_address['street_address'])

    def test_create(self):

        main_address = {
            'street_address': 'no 2 olugbede street idumu, lagos',
            'country': 'Nigeria',
            'city': 'Lagos',
            'zip_code': '35464',
        }

        response = self.client.post('/address/', main_address)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data['street_address'], main_address['street_address'])

    def test_delete(self):

        response = self.client.delete('/address/1/')

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(Address.DoesNotExist):
            Address.objects.get(pk=1)

    def test_retrieve(self):
        response = self.client.get('/address/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['street_address'], self.main_address['street_address'])

    def test_user_addresses(self):

        response = self.client.get('/buyer/users/addresses/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data[0]['street_address'], self.main_address['street_address'])
