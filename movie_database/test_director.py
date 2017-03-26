from django.core.exceptions import ValidationError
from django.test import TestCase

from movie_database.models import Actor


class ActorTestCase(TestCase):
    def test_empty_name_should_throw_error(self):
        actor = Actor()
        with self.assertRaises(ValidationError):
            actor.full_clean()

    def test_empty_name_should_throw_error(self):
        actor = Actor(surname='spilberg')
        with self.assertRaises(ValidationError):
            actor.full_clean()

    def test_empty_surname_should_throw_error(self):
        actor = Actor(name='ennio')
        with self.assertRaises(ValidationError):
            actor.full_clean()

    def test_too_long_name_should_throw_error(self):
        actor = Actor(name='a' * 21, surname='spilberg')
        with self.assertRaises(ValidationError):
            actor.full_clean()

    def test_too_long_surname_should_throw_error(self):
        actor = Actor(name='steven', surname='a' * 41)
        with self.assertRaises(ValidationError):
            actor.full_clean()

    def test_saving_actor_no_error_throw(self):
        actor = Actor(name='steven', surname='spilberg')
        actor.full_clean()
        actor.save()
        self.assertEqual(1, actor.id)
        self.assertEqual('steven', actor.name)
        self.assertEqual('spilberg', actor.surname)
        self.assertIsNotNone(actor.created)

    def test_updating_name_no_error_throw(self):
        actor = Actor(name='ennio', surname='spilberg')
        actor.full_clean()
        actor.save()
        created_date_src = actor.created

        actor.name = 'steven'
        actor.save()
        actor.full_clean()
        actor.refresh_from_db()
        created_date_dest = actor.created

        self.assertEqual(Actor.objects.count(), 1)
        self.assertEqual(1, actor.id)
        self.assertEqual('steven', actor.name)
        self.assertEqual('spilberg', actor.surname)
        self.assertEqual(created_date_dest, created_date_src)

    def test_updating_surname_no_error_throw(self):
        actor = Actor(name='ennio', surname='spilberg')
        actor.full_clean()
        actor.save()

        actor.surname = 'McDoe'
        actor.save()
        actor.full_clean()
        actor.refresh_from_db()

        self.assertEqual(Actor.objects.count(), 1)
        self.assertEqual(1, actor.id)
        self.assertEqual('ennio', actor.name)
        self.assertEqual('McDoe', actor.surname)

    def test_updating_name_validation_throw(self):
        actor = Actor(name='steven', surname='spilberg')
        actor.full_clean()
        actor.save()

        actor.name = 'a' * 21
        with self.assertRaises(ValidationError):
            actor.full_clean()

    def test_updating_surname_validation_throw(self):
        actor = Actor(name='steven', surname='spilberg')
        actor.full_clean()
        actor.save()

        actor.surname = 'a' * 41
        with self.assertRaises(ValidationError):
            actor.full_clean()

    def test_updating_name_none_should_validation_error_throw(self):
        actor = Actor(name='steven', surname='spilberg')
        actor.full_clean()
        actor.save()

        actor.name = None
        with self.assertRaises(ValidationError):
            actor.full_clean()

    def test_updating_surname_none_should_validation_error_throw(self):
        actor = Actor(name='steven', surname='spilberg')
        actor.full_clean()
        actor.save()

        actor.surname = None
        with self.assertRaises(ValidationError):
            actor.full_clean()

    def test_deleting_existing_actor_should_pass(self):
        actor = Actor(name='steven', surname='spilberg')
        actor.save()

        actor.delete()
        self.assertEqual(0, Actor.objects.count())

    def test_deleting_none_existing_actor_should_error_throw(self):
        actor = Actor(name='steven', surname='spilberg')

        with self.assertRaises(AssertionError):
            actor.delete()
