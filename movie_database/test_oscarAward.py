from django.core.exceptions import ValidationError
from django.test import TestCase

from movie_database.models import OscarAward, oscar_categories_tuple


class OscarAwardTestCase(TestCase):
    def test_empty_award_should_throw_error(self):
        oscarAward = OscarAward()
        with self.assertRaises(ValidationError):
            oscarAward.full_clean()

    def test_wrong_category_should_throw_error(self):
        oscarAward = OscarAward(category='AA')
        with self.assertRaises(ValidationError):
            oscarAward.full_clean()

    def test_wrong_year_should_throw_error(self):
        oscarAward = OscarAward(year=1900, category=oscar_categories_tuple[0][0])
        with self.assertRaises(ValidationError):
            oscarAward.full_clean()

    def test_future_year_should_throw_error(self):
        oscarAward = OscarAward(year=2030, category=oscar_categories_tuple[0][0])
        with self.assertRaises(ValidationError):
            oscarAward.full_clean()

    def test_saving_oscar_no_error_throw(self):
        oscarAward = OscarAward(year=1979, category=oscar_categories_tuple[0][0])
        oscarAward.full_clean()
        oscarAward.save()
        self.assertEqual(1, oscarAward.id)
        self.assertEqual(1979, oscarAward.year)
        self.assertEqual('Best_Film', oscarAward.category)

    def test_updating_year_no_error_throw(self):
        oscarAward = OscarAward(year=1979, category=oscar_categories_tuple[0][0])
        oscarAward.full_clean()
        oscarAward.save()

        oscarAward.year = 1989
        oscarAward.save()
        oscarAward.full_clean()
        oscarAward.refresh_from_db()

        self.assertEqual(1, oscarAward.id)
        self.assertEqual(1989, oscarAward.year)
        self.assertEqual('Best_Film', oscarAward.category)

    def test_updating_year_throw_error(self):
        oscarAward = OscarAward(year=1979, category=oscar_categories_tuple[0][0])
        oscarAward.full_clean()
        oscarAward.save()

        oscarAward.year = 1900
        with self.assertRaises(ValidationError):
            oscarAward.full_clean()

    def test_updating_future_year_throw_error(self):
        oscarAward = OscarAward(year=1979, category=oscar_categories_tuple[0][0])
        oscarAward.full_clean()
        oscarAward.save()

        oscarAward.year = 2018
        with self.assertRaises(ValidationError):
            oscarAward.full_clean()

    def test_updating_category_throw_error(self):
        oscarAward = OscarAward(year=1979, category=oscar_categories_tuple[0][0])
        oscarAward.full_clean()
        oscarAward.save()

        oscarAward.year = 'AA'
        with self.assertRaises(ValidationError):
            oscarAward.full_clean()

    def test_updating_category_no_validation_throw(self):
        oscarAward = OscarAward(year=1979, category=oscar_categories_tuple[0][0])
        oscarAward.full_clean()
        oscarAward.save()

        oscarAward.category = oscar_categories_tuple[1][0]
        self.assertEqual(1, oscarAward.id)
        self.assertEqual(1979, oscarAward.year)
        self.assertEqual('Best_Film_Editing', oscarAward.category)
