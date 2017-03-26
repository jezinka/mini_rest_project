from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from movie_database.models import OscarAward, oscar_categories_tuple


class TestOscarAwardViewSet(APITestCase):
    def test_detail_view_with_a_non_exist_oscarAward(self):
        # should return a 404 not found.
        url = reverse('oscaraward-detail', kwargs={'pk': 123})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_list_view_for_empty_oscarAwards(self):
        # should return 200 OK
        response = self.client.get('/oscarAwards/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #
    def test_create_new_valid_oscarAward(self):
        url = reverse('oscaraward-list')
        data = {'category': oscar_categories_tuple[0][0], 'year': 2010}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OscarAward.objects.count(), 1)
        self.assertEqual(OscarAward.objects.get().category, 'Best_Film')
        self.assertEqual(OscarAward.objects.get().year, 2010)

    def test_create_new_empty_category_oscarAward_should_throw_400(self):
        url = reverse('oscaraward-list')
        data = {'category': None, 'year': 2010}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(OscarAward.objects.count(), 0)

    def test_create_new_empty_year_oscarAward_should_throw_400(self):
        url = reverse('oscaraward-list')
        data = {'category': oscar_categories_tuple[0][0], 'year': None}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(OscarAward.objects.count(), 0)

    def test_detail_view_with_a_exist_oscarAward(self):
        # should return a 200 OK
        g = OscarAward(category=oscar_categories_tuple[0][0], year=2010)
        g.save()

        url = reverse('oscaraward-detail', kwargs={'pk': g.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_edit_category_valid_oscarAward(self):
        g = OscarAward(category=oscar_categories_tuple[0][0], year=2010)
        g.save()
        url = reverse('oscaraward-detail', kwargs={'pk': g.id})
        data = {'category': oscar_categories_tuple[1][0]}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OscarAward.objects.count(), 1)
        self.assertEqual(OscarAward.objects.get().category, 'Best_Film_Editing')
        self.assertEqual(OscarAward.objects.get().year, 2010)

    def test_edit_year_valid_oscarAward(self):
        g = OscarAward(category=oscar_categories_tuple[0][0], year=2010)
        g.save()
        url = reverse('oscaraward-detail', kwargs={'pk': g.id})
        data = {'year': 2007}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OscarAward.objects.count(), 1)
        self.assertEqual(OscarAward.objects.get().year, 2007)
        self.assertEqual(OscarAward.objects.get().category, 'Best_Film')

    def test_delete_oscarAward(self):
        g = OscarAward(category=oscar_categories_tuple[0][0], year=2010)
        g.save()
        url = reverse('oscaraward-detail', kwargs={'pk': g.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(OscarAward.objects.count(), 0)

    def test_list_view_for_oscarAwards(self):
        # should return 200 OK
        g = OscarAward(category=oscar_categories_tuple[0][0], year=2010)
        g.save()
        response = self.client.get('/oscarAwards/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
