from django.core.exceptions import ValidationError
from django.test import TestCase

from movie_database.models import Movie, Director, Actor, oscar_categories_tuple, OscarAward


class MovieTestCase(TestCase):
    def setUp(self):
        Director(name='Stephen', surname='Spilberg').save()
        Director(name='Peter', surname='Jackson').save()
        Actor(name='Leonardo', surname='diCaprio').save()
        Actor(name='Anna', surname='Dymna').save()
        OscarAward(year=1979, category=oscar_categories_tuple[0][0]).save()
        OscarAward(year=1999, category=oscar_categories_tuple[3][0]).save()

    def test_empty_director_should_throw_error(self):
        movie = Movie()
        with self.assertRaises(ValidationError):
            movie.full_clean()

    def test_empty_title_should_throw_error(self):
        movie = Movie(director=Director.objects.get(pk=1))
        with self.assertRaises(ValidationError):
            movie.full_clean()

    def test_too_long_title_should_throw_error(self):
        movie = Movie(director=Director.objects.get(pk=1),
                      title='a' * 101)
        with self.assertRaises(ValidationError):
            movie.full_clean()

    def test_saving_movie_no_error_throw(self):
        movie = Movie(title='IT Crowd', director=Director.objects.get(pk=1))
        movie.full_clean()
        movie.save()
        self.assertEqual(1, movie.id)
        self.assertEqual('IT Crowd', movie.title)
        self.assertEqual(movie.director, Director.objects.get(pk=1))
        self.assertIsNotNone(movie.created)

    def test_updating_title_no_error_throw(self):
        movie = Movie(title='Silicon Valley', director=Director.objects.get(pk=1))
        movie.full_clean()
        movie.save()
        created_date_src = movie.created

        movie.title = 'IT Crowd'
        movie.save()
        movie.full_clean()
        movie.refresh_from_db()
        created_date_dest = movie.created

        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(1, movie.id)
        self.assertEqual('IT Crowd', movie.title)
        self.assertEqual(Director.objects.get(pk=1), movie.director)
        self.assertEqual(created_date_dest, created_date_src)

    def test_updating_director_no_error_throw(self):
        movie = Movie(title='IT Crowd', director=Director.objects.get(pk=1))
        movie.full_clean()
        movie.save()
        created_date_src = movie.created

        movie.director = Director.objects.get(pk=2)
        movie.save()
        movie.full_clean()
        movie.refresh_from_db()
        created_date_dest = movie.created

        self.assertEqual(Movie.objects.count(), 1)
        self.assertEqual(1, movie.id)
        self.assertEqual('IT Crowd', movie.title)
        self.assertEqual(Director.objects.get(pk=2), movie.director)
        self.assertEqual(created_date_dest, created_date_src)

    def test_updating_title_validation_throw(self):
        movie = Movie(title='IT Crowd', director=Director.objects.get(pk=1))
        movie.full_clean()
        movie.save()

        movie.title = 'a' * 101
        with self.assertRaises(ValidationError):
            movie.full_clean()

    def test_updating_director_validation_throw(self):
        movie = Movie(title='IT Crowd', director=Director.objects.get(pk=1))
        movie.full_clean()
        movie.save()

        with self.assertRaises(ValueError):
            movie.director = None

    def test_updating_title_none_should_validation_error_throw(self):
        movie = Movie(title='IT Crowd', director=Director.objects.get(pk=1))
        movie.full_clean()
        movie.save()

        movie.title = None
        with self.assertRaises(ValidationError):
            movie.full_clean()

    def test_deleting_existing_movie_should_pass(self):
        movie = Movie(title='IT Crowd', director=Director.objects.get(pk=1))
        movie.save()

        movie.delete()
        self.assertEqual(0, Movie.objects.count())

    def test_deleting_none_existing_movie_should_error_throw(self):
        movie = Movie(title='IT Crowd')

        with self.assertRaises(AssertionError):
            movie.delete()

    def test_saving_movie_with_actors_no_error_throw(self):
        movie = Movie(title='IT Crowd', director=Director.objects.get(pk=1))
        movie.full_clean()
        movie.save()
        movie.actor.add(Actor.objects.get(pk=1))
        movie.save()
        self.assertEqual(1, movie.id)
        self.assertEqual('IT Crowd', movie.title)
        self.assertEqual(movie.director, Director.objects.get(pk=1))
        self.assertEqual(movie.actor.all()[0], Actor.objects.get(pk=1))
        self.assertIsNotNone(movie.created)

    def test_updated_movie_with_actors_no_error_throw(self):
        movie = Movie(title='IT Crowd', director=Director.objects.get(pk=1))
        movie.full_clean()
        movie.save()
        movie.actor.add(Actor.objects.get(pk=1))
        movie.save()
        movie.actor.add(Actor.objects.get(pk=2))
        movie.save()
        self.assertEqual(1, movie.id)
        self.assertEqual('IT Crowd', movie.title)
        self.assertEqual(movie.director, Director.objects.get(pk=1))
        self.assertEqual(len(movie.actor.all()), 2)
        self.assertQuerysetEqual(movie.actor.all(), [repr(r) for r in Actor.objects.all()])
        self.assertIsNotNone(movie.created)

    def test_saving_movie_boolean_true_no_error_throw(self):
        movie = Movie(title='IT Crowd', director=Director.objects.get(pk=1), animated=True)
        movie.full_clean()
        movie.save()
        self.assertEqual(1, movie.id)
        self.assertEqual('IT Crowd', movie.title)
        self.assertEqual(movie.director, Director.objects.get(pk=1))
        self.assertTrue(movie.animated)
        self.assertIsNotNone(movie.created)

    def test_saving_movie_boolean_false_no_error_throw(self):
        movie = Movie(title='IT Crowd', director=Director.objects.get(pk=1), animated=False)
        movie.full_clean()
        movie.save()
        self.assertEqual(1, movie.id)
        self.assertEqual('IT Crowd', movie.title)
        self.assertEqual(movie.director, Director.objects.get(pk=1))
        self.assertFalse(movie.animated)
        self.assertIsNotNone(movie.created)

    def test_update_movie_boolean_no_error_throw(self):
        movie = Movie(title='IT Crowd', director=Director.objects.get(pk=1), animated=False)
        movie.full_clean()
        movie.save()
        movie.animated = True
        self.assertEqual(1, movie.id)
        self.assertEqual('IT Crowd', movie.title)
        self.assertEqual(movie.director, Director.objects.get(pk=1))
        self.assertTrue(movie.animated)
        self.assertIsNotNone(movie.created)

    def test_saving_movie_oscar_award_no_error_throw(self):
        movie = Movie(title='IT Crowd', director=Director.objects.get(pk=1))
        movie.full_clean()
        movie.save()
        movie.oscar_award = OscarAward.objects.get(pk=1)
        movie.save()
        self.assertEqual(1, movie.id)
        self.assertEqual('IT Crowd', movie.title)
        self.assertEqual(movie.director, Director.objects.get(pk=1))
        self.assertTrue(movie.oscar_award, OscarAward.objects.get(pk=1))
        self.assertIsNotNone(movie.created)

    def test_editing_movie_oscar_award_no_error_throw(self):
        movie = Movie(title='IT Crowd', director=Director.objects.get(pk=1))
        movie.full_clean()
        movie.save()
        movie.oscar_award = OscarAward.objects.get(pk=1)
        movie.save()
        movie.oscar_award = OscarAward.objects.get(pk=2)
        movie.save()
        self.assertEqual(1, movie.id)
        self.assertEqual('IT Crowd', movie.title)
        self.assertEqual(movie.director, Director.objects.get(pk=1))
        self.assertTrue(movie.oscar_award, OscarAward.objects.get(pk=2))
        self.assertIsNotNone(movie.created)
