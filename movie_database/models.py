from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models

oscar_categories = ['Best Film', 'Best Film Editing', 'Best Scenario', 'Best Adapter Screenplay', 'Best Original Song']
oscar_categories_tuple = [(f.replace(' ', '_'), f) for f in oscar_categories]


class Genre(models.Model):
    name = models.CharField(max_length=10, validators=[MinLengthValidator(1)])


class OscarAward(models.Model):
    category = models.CharField(max_length=20, choices=oscar_categories_tuple, null=False)
    year = models.IntegerField(validators=[MinValueValidator(1929), MaxValueValidator(2016)])


class Actor(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=20, blank=False)
    surname = models.CharField(max_length=40, blank=False)

    class Meta:
        ordering = ('surname', 'name')
