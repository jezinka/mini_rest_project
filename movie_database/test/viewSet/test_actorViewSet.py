from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from movie_database.models import Actor, Director, Movie


class TestActorViewSet(APITestCase):
    def test_detail_view_with_a_non_exist_actor(self):
        # should return a 404 not found.
        url = reverse('actor-detail', kwargs={'pk': 123})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_list_view_for_empty_actors(self):
        # should return 200 OK
        response = self.client.get('/actors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_new_valid_actor(self):
        url = reverse('actor-list')
        data = {'name': 'jane', 'surname': 'doe'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Actor.objects.count(), 1)
        self.assertEqual(Actor.objects.get().name, 'jane')
        self.assertEqual(Actor.objects.get().surname, 'doe')

    def test_create_new_empty_name_actor_should_throw_400(self):
        url = reverse('actor-list')
        data = {'name': None, 'surname': 'doe'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Actor.objects.count(), 0)

    def test_create_new_empty_surname_actor_should_throw_400(self):
        url = reverse('actor-list')
        data = {'name': 'jane', 'surname': None}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Actor.objects.count(), 0)

    def test_detail_view_with_a_exist_actor(self):
        # should return a 200 OK
        g = Actor(name='jane', surname='doe')
        g.save()

        url = reverse('actor-detail', kwargs={'pk': g.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_name_valid_actor(self):
        g = Actor(name='jane', surname='doe')
        g.save()
        url = reverse('actor-detail', kwargs={'pk': g.id})
        data = {'name': 'john'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Actor.objects.count(), 1)
        self.assertEqual(Actor.objects.get().name, 'john')
        self.assertEqual(Actor.objects.get().surname, 'doe')

    def test_edit_surname_valid_actor(self):
        g = Actor(name='jane', surname='doe')
        g.save()
        url = reverse('actor-detail', kwargs={'pk': g.id})
        data = {'surname': 'doe'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Actor.objects.count(), 1)
        self.assertEqual(Actor.objects.get().surname, 'doe')
        self.assertEqual(Actor.objects.get().name, 'jane')

    def test_delete_actor(self):
        g = Actor(name='jane', surname='doe')
        g.save()
        url = reverse('actor-detail', kwargs={'pk': g.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Actor.objects.count(), 0)

    def test_list_view_for_actors(self):
        # should return 200 OK
        g = Actor(name='jane', surname='doe')
        g.save()
        response = self.client.get('/actors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_directs_related_property_from_movie(self):
        Director(name='steven', surname='spilberg').save()

        a1 = Actor(name='Leonardo', surname='diCaprio')
        a1.save()
        a2 = Actor(name='Bill', surname='Murray')
        a2.save()

        m1 = Movie(title='Logan', director=Director.objects.get(pk=1))
        m1.save()
        m1.actor.add(a1)
        m1.save()

        m2 = Movie(title='Top Gun', director=Director.objects.get(pk=1))
        m2.save()
        m1.actor.add(a2)
        m1.save()

        url = reverse('actor-detail', kwargs={'pk': 2})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['id'], 2)
        self.assertEqual(response.data['name'], 'Bill')
        self.assertEqual(response.data['surname'], 'Murray')
        self.assertEqual(len(response.data['plays']), 1)

    def test_delete_actor_not_deletes_movies(self):
        Director(name='steven', surname='spilberg').save()
        m = Movie(title='Logan', director=Director.objects.get(pk=1))
        m.save()

        a = Actor(name='Bill', surname='Murray')
        a.save()
        m.actor.add(a)
        m.save()

        url = reverse('actor-detail', kwargs={'pk': a.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Actor.objects.count(), 0)
        self.assertEqual(Movie.objects.count(), 1)
