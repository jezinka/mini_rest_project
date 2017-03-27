from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

oscar_categories = ['Best Film', 'Best Film Editing', 'Best Scenario', 'Best Adapter Screenplay', 'Best Original Song']
oscar_categories_tuple = [(f.replace(' ', '_'), f) for f in oscar_categories]


class Genre(models.Model):
    name = models.CharField(max_length=10, validators=[MinLengthValidator(1)])

    def __str__(self):
        return '%s' % (self.name)

class OscarAward(models.Model):
    category = models.CharField(max_length=20, choices=oscar_categories_tuple, null=False)
    year = models.IntegerField(validators=[MinValueValidator(1929), MaxValueValidator(2016)])

    class Meta:
        unique_together = ('category', 'year')

    def __str__(self):
        return '%s %d' % (self.category, self.year)


class Actor(models.Model):
    # should be inheritance from Person
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=20, blank=False)
    surname = models.CharField(max_length=40, blank=False)

    class Meta:
        ordering = ('surname', 'name')

    def __str__(self):
        return '%s %s' % (self.name, self.surname)


class Director(models.Model):
    # should be inheritance from Person
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=20, blank=False)
    surname = models.CharField(max_length=40, blank=False)

    class Meta:
        ordering = ('surname', 'name')

    def __str__(self):
        return '%s %s' % (self.name, self.surname)


class Movie(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, validators=[MinLengthValidator(1)])
    director = models.ForeignKey(Director, related_name='directs', null=False)
    actor = models.ManyToManyField(Actor, related_name='plays')
    oscar_award = models.OneToOneField(OscarAward, on_delete=models.SET_NULL, null=True, blank=True)
    animated = models.BooleanField(default=False)
    genre = models.ManyToManyField(Genre, related_name='movie_genre')

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return '%s' % (self.title)
