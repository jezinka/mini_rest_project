from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from movie_database.models import Genre


class TestGenreViewSet(APITestCase):
    def test_detail_view_with_a_non_exist_genre(self):
        # should return a 404 not found.
        response = self.client.get('/genre/4/')
        self.assertEqual(response.status_code, 404)

    def test_list_view_for_empty_genres(self):
        # should return 200 OK
        response = self.client.get('/genres/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_valid_genre(self):
        url = reverse('genre-list')
        data = {'name': 'Comedy'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Genre.objects.count(), 1)
        self.assertEqual(Genre.objects.get().name, 'Comedy')

    def test_create_new_empty_genre_should_throw_400(self):
        url = reverse('genre-list')
        data = {'name': None}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Genre.objects.count(), 0)

    def test_edit_new_valid_genre(self):
        g = Genre(name='Comedy')
        g.save()
        url = reverse('genre-detail', kwargs={'pk': g.id})
        data = {'name': 'Horror'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Genre.objects.count(), 1)
        self.assertEqual(Genre.objects.get().name, 'Horror')

    def test_delete_genre(self):
        g = Genre(name='Horror')
        g.save()
        url = reverse('genre-detail', kwargs={'pk': g.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Genre.objects.count(), 0)
