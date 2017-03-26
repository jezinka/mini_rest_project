from rest_framework import serializers

from movie_database.models import Genre


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ('url', 'id', 'name')
