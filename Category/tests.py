from rest_framework.test import APITestCase

from .models import Category


class CategoryTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):

        fashion = Category.objects.create(name='fashion')
        men_clothing = Category.objects.create(
            name='men_clothing', parent=fashion)
        jean_category = Category.objects.create(
            name='jeans', parent=men_clothing)

        electronics = Category.objects.create(name='electronic')
        note_books = Category.objects.create(
            name='note_book', parent=electronics)
        laptop = Category.objects.create(name='laptop', parent=note_books)

    def test_categories(self):
        response = self.client.get('/categories/')

        self.assertEqual(response.status_code, 200)
