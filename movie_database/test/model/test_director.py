from django.core.exceptions import ValidationError
from django.test import TestCase

from movie_database.models import Director, Movie


class DirectorTestCase(TestCase):

    def test_empty_name_should_throw_error(self):
        director = Director()
        with self.assertRaises(ValidationError):
            director.full_clean()

    def test_empty_name_should_throw_error(self):
        director = Director(surname='spilberg')
        with self.assertRaises(ValidationError):
            director.full_clean()

    def test_empty_surname_should_throw_error(self):
        director = Director(name='ennio')
        with self.assertRaises(ValidationError):
            director.full_clean()

    def test_too_long_name_should_throw_error(self):
        director = Director(name='a' * 21, surname='spilberg')
        with self.assertRaises(ValidationError):
            director.full_clean()

    def test_too_long_surname_should_throw_error(self):
        director = Director(name='steven', surname='a' * 41)
        with self.assertRaises(ValidationError):
            director.full_clean()

    def test_saving_director_no_error_throw(self):
        director = Director(name='steven', surname='spilberg')
        director.full_clean()
        director.save()
        self.assertEqual(1, director.id)
        self.assertEqual('steven', director.name)
        self.assertEqual('spilberg', director.surname)
        self.assertIsNotNone(director.created)

    def test_updating_name_no_error_throw(self):
        director = Director(name='ennio', surname='spilberg')
        director.full_clean()
        director.save()
        created_date_src = director.created

        director.name = 'steven'
        director.save()
        director.full_clean()
        director.refresh_from_db()
        created_date_dest = director.created

        self.assertEqual(Director.objects.count(), 1)
        self.assertEqual(1, director.id)
        self.assertEqual('steven', director.name)
        self.assertEqual('spilberg', director.surname)
        self.assertEqual(created_date_dest, created_date_src)

    def test_updating_surname_no_error_throw(self):
        director = Director(name='ennio', surname='spilberg')
        director.full_clean()
        director.save()

        director.surname = 'McDoe'
        director.save()
        director.full_clean()
        director.refresh_from_db()

        self.assertEqual(Director.objects.count(), 1)
        self.assertEqual(1, director.id)
        self.assertEqual('ennio', director.name)
        self.assertEqual('McDoe', director.surname)

    def test_updating_name_validation_throw(self):
        director = Director(name='steven', surname='spilberg')
        director.full_clean()
        director.save()

        director.name = 'a' * 21
        with self.assertRaises(ValidationError):
            director.full_clean()

    def test_updating_surname_validation_throw(self):
        director = Director(name='steven', surname='spilberg')
        director.full_clean()
        director.save()

        director.surname = 'a' * 41
        with self.assertRaises(ValidationError):
            director.full_clean()

    def test_updating_name_none_should_validation_error_throw(self):
        director = Director(name='steven', surname='spilberg')
        director.full_clean()
        director.save()

        director.name = None
        with self.assertRaises(ValidationError):
            director.full_clean()

    def test_updating_surname_none_should_validation_error_throw(self):
        director = Director(name='steven', surname='spilberg')
        director.full_clean()
        director.save()

        director.surname = None
        with self.assertRaises(ValidationError):
            director.full_clean()

    def test_deleting_existing_director_should_pass(self):
        director = Director(name='steven', surname='spilberg')
        director.save()

        director.delete()
        self.assertEqual(0, Director.objects.count())

    def test_deleting_none_existing_director_should_error_throw(self):
        director = Director(name='steven', surname='spilberg')

        with self.assertRaises(AssertionError):
            director.delete()

    def test_deleting_existing_director_should_remove_movie(self):
        director = Director(name='steven', surname='spilberg')
        director.save()
        movie = Movie(title='IT Crowd', director=Director.objects.get(pk=1))
        movie.save()

        director.delete()
        self.assertEqual(0, Director.objects.count())
        self.assertEqual(0, Movie.objects.count())
