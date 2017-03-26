from rest_framework import serializers

from movie_database.models import Genre, OscarAward


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ('url', 'id', 'name')


class OscarAwardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OscarAward
        fields = ('url', 'id', 'category', 'year')
