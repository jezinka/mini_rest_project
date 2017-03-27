from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from movie_database.models import Director, Actor, OscarAward, oscar_categories_tuple, Movie


class TestMovieViewSet(APITestCase):
    def setUp(self):
        Director(name='Stephen', surname='Spilberg').save()
        Director(name='Peter', surname='Jackson').save()
        Actor(name='Leonardo', surname='diCaprio').save()
        Actor(name='Anna', surname='Dymna').save()
        OscarAward(year=1979, category=oscar_categories_tuple[0][0]).save()
        OscarAward(year=1999, category=oscar_categories_tuple[3][0]).save()

    def test_detail_view_with_a_non_exist_movie(self):
        # should return a 404 not found.
        url = reverse('movie-detail', kwargs={'pk': 123})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_list_view_for_empty_movies(self):
        # should return 200 OK
        url = reverse('movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_valid_movie(self):
        url = reverse('movie-list')
        data = {'title': 'steven', 'director': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(Movie.objects.get().title, 'steven')
        self.assertEqual(Movie.objects.get().director, Director.objects.get(pk=1))
