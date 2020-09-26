from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from Users.permissions import create_user_permissions

from Users.models.address import Address
from .models.shipping_detail import ShippingDetail
from .models.profile import BuyerProfile

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
        cls.buyer = BuyerProfile.objects.create(user=cls.user)

        token = 'JWT ' + cls.user.token

        cls.b_token = token.encode()

        cls.main_address = {
            'first_name': 'Duke',
            'last_name': 'Effiom',
            'phone_number': '+2347037606116',
            '[address][address]': 'no 34 beckham street, ikeja Lagos',
            '[address][country]': 'Nigeria',
            '[address][city]': 'Lagos',
            '[address][state]': 'Lagos',
            '[address][zip_code]': '35467',
        }

        cls.main_address_2 = {
            'address': 'no 2 olugbede street idumu, lagos',
            'country': 'Nigeria',
            'city': 'Ikeja',
            'state': 'Lagos',
            'zip_code': '35464',
        }

        address_obj = Address.objects.create(**cls.main_address_2)

        ShippingDetail.objects.create(
            buyer=cls.buyer,
            address=address_obj,
            first_name="duke",
            last_name='Effiom',
            phone_number='+2347037606116'
            )

    def setUp(self):

        self.client.credentials(HTTP_AUTHORIZATION=self.b_token)

    def test_create(self):

        response = self.client.post('/shipping/', self.main_address)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data['address']['address'], 
            self.main_address['[address][address]']
            )

    def test_update(self):

        address = {
            'first_name': 'Duke',
            'last_name': 'Effiom',
            'phone_number': '+2347037606116',
            '[address][address]': 'no 34 beckham street, ikeja Abuja',
            '[address][city]': 'Abuja',
            '[address][state]': 'Lagos',
            '[address][zip_code]': '35467',
        }

        response = self.client.patch('/shipping/1/', address, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['address']['address'],
            address['[address][address]']
        )

    def test_list(self):

        response = self.client.get('/shipping/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data[0]['address']['address'], 
            self.main_address_2['address']
            )

    def test_retrieve(self):
        response = self.client.get('/shipping/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data['address']['address'],
            self.main_address_2['address']
        )

    def test_delete(self):

        response = self.client.delete('/shipping/1/')

        self.assertEqual(response.status_code, 204)
        with self.assertRaises(ShippingDetail.DoesNotExist):
            ShippingDetail.objects.get(pk=1)

    
