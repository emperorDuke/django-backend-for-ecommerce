from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile

from rest_framework.test import APITestCase

from Stores.models.store import Store

from Users.permissions import create_user_permissions

from Adverts.models import Advert


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
