from rest_framework import serializers

from movie_database.models import Genre, OscarAward, Actor, Director, Movie


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Genre
        fields = ('url', 'id', 'name')


class OscarAwardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OscarAward
        fields = ('url', 'id', 'category', 'year')


class ActorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Actor
        fields = ('url', 'id', 'name', 'surname', 'created')


class DirectorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Director
        fields = ('url', 'id', 'name', 'surname', 'created')


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Movie
        fields = ('url', 'id', 'title', 'director', 'actor', 'oscar_award', 'animated')
