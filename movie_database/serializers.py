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
    plays = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='movie-detail'
    )

    class Meta:
        model = Actor
        fields = ('url', 'id', 'name', 'surname', 'created', 'plays')


class DirectorSerializer(serializers.HyperlinkedModelSerializer):
    directs = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='movie-detail'
    )

    class Meta:
        model = Director
        fields = ('url', 'id', 'name', 'surname', 'created', 'directs')


class MovieSerializer(serializers.HyperlinkedModelSerializer):
    director = serializers.PrimaryKeyRelatedField(queryset=Director.objects.all(), many=False, read_only=False)
    actor = serializers.PrimaryKeyRelatedField(queryset=Actor.objects.all(), many=True, read_only=False)

    class Meta:
        model = Movie
        fields = ('url', 'id', 'title', 'director', 'actor', 'oscar_award', 'animated')
