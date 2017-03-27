from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from movie_database.models import Actor


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
