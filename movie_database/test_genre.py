from django.test import TestCase
from django.core.exceptions import ValidationError
from movie_database.models import Genre


class GenreTestCase(TestCase):
    def test_empty_name_should_throw_error(self):
        genre = Genre()
        with self.assertRaises(ValidationError):
            genre.full_clean()

    def test_too_long_name_should_throw_error(self):
        genre = Genre(name='a' * 11)
        with self.assertRaises(ValidationError):
            genre.full_clean()

    def test_saving_name_no_error_throw(self):
        genre = Genre(name='Comedy')
        genre.full_clean()
        genre.save()
        self.assertEqual(1, genre.id)
        self.assertEqual('Comedy', genre.name)

    def test_updating_name_no_error_throw(self):
        genre = Genre(name='Thriller')
        genre.full_clean()
        genre.save()

        genre.name = 'Horror'
        genre.save()
        genre.full_clean()
        genre.refresh_from_db()

        self.assertEqual(Genre.objects.count(), 1)
        self.assertEqual(1, genre.id)
        self.assertEqual('Horror', genre.name)

    def test_updating_name_validation_throw(self):
        genre = Genre(name='Thriller')
        genre.full_clean()
        genre.save()

        genre.name = 'a' * 11
        with self.assertRaises(ValidationError):
            genre.full_clean()

    def test_updating_name_no_validation_throw(self):
        genre = Genre(name='Thriller')
        genre.full_clean()
        genre.save()

        genre.name = None
        with self.assertRaises(ValidationError):
            genre.full_clean()
