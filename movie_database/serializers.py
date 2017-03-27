from rest_framework import serializers

from movie_database.models import Genre, OscarAward, Actor, Director, Movie


class GenreSerializer(serializers.HyperlinkedModelSerializer):
    movie_genre = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='movie-detail'
    )

    class Meta:
        model = Genre
        fields = ('url', 'id', 'name', 'movie_genre')


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
    actor = serializers.PrimaryKeyRelatedField(default=[], queryset=Actor.objects.all(), many=True, read_only=False,
                                               allow_empty=True)
    genre = serializers.PrimaryKeyRelatedField(default=[], queryset=Genre.objects.all(), many=True, read_only=False,
                                               allow_empty=True)

    class Meta:
        model = Movie
        fields = ('url', 'id', 'title', 'genre', 'director', 'actor', 'oscar_award', 'animated')
