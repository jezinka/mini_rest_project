from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator

oscar_categories = ['Best Film', 'Best Film Editing', 'Best Scenario', 'Best Adapter Screenplay', 'Best Original Song']
oscar_categories_tuple = [(f.replace(' ', '_'), f) for f in oscar_categories]


class Genre(models.Model):
    name = models.CharField(max_length=10, validators=[MinLengthValidator(1)])
