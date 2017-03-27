from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from movie_database.models import Director


class TestDirectorViewSet(APITestCase):
    def test_detail_view_with_a_non_exist_director(self):
        # should return a 404 not found.
        url = reverse('director-detail', kwargs={'pk': 123})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_list_view_for_empty_directors(self):
        # should return 200 OK
        response = self.client.get('/directors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_valid_director(self):
        url = reverse('director-list')
        data = {'name': 'steven', 'surname': 'spilberg'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Director.objects.count(), 1)
        self.assertEqual(Director.objects.get().name, 'steven')
        self.assertEqual(Director.objects.get().surname, 'spilberg')

    def test_create_new_empty_name_director_should_throw_400(self):
        url = reverse('director-list')
        data = {'name': None, 'surname': 'spilberg'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Director.objects.count(), 0)

    def test_create_new_empty_surname_director_should_throw_400(self):
        url = reverse('director-list')
        data = {'name': 'steven', 'surname': None}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Director.objects.count(), 0)

    def test_detail_view_with_a_exist_director(self):
        # should return a 200 OK
        g = Director(name='steven', surname='spilberg')
        g.save()

        url = reverse('director-detail', kwargs={'pk': g.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['name'], 'steven')
        self.assertEqual(response.data['surname'], 'spilberg')

    def test_edit_name_valid_director(self):
        g = Director(name='steven', surname='spilberg')
        g.save()
        url = reverse('director-detail', kwargs={'pk': g.id})
        data = {'name': 'ennio'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Director.objects.count(), 1)
        self.assertEqual(Director.objects.get().name, 'ennio')
        self.assertEqual(Director.objects.get().surname, 'spilberg')

    def test_edit_surname_valid_director(self):
        g = Director(name='steven', surname='spilberg')
        g.save()
        url = reverse('director-detail', kwargs={'pk': g.id})
        data = {'surname': 'spilberg'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Director.objects.count(), 1)
        self.assertEqual(Director.objects.get().surname, 'spilberg')
        self.assertEqual(Director.objects.get().name, 'steven')

    def test_delete_director(self):
        g = Director(name='steven', surname='spilberg')
        g.save()
        url = reverse('director-detail', kwargs={'pk': g.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Director.objects.count(), 0)

    def test_list_view_for_directors(self):
        # should return 200 OK
        g = Director(name='steven', surname='spilberg')
        g = Director(name='steven', surname='spilberg')
        g.save()
        response = self.client.get('/directors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
