from rest_framework import viewsets

from movie_database.models import Genre, OscarAward, Actor, Director, Movie
from movie_database.serializers import GenreSerializer, OscarAwardSerializer, ActorSerializer, DirectorSerializer, \
    MovieSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def perform_create(self, serializer):
        serializer.save()


class OscarAwardViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = OscarAward.objects.all()
    serializer_class = OscarAwardSerializer

    def perform_create(self, serializer):
        serializer.save()


class ActorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def perform_create(self, serializer):
        serializer.save()


class DirectorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

    def perform_create(self, serializer):
        serializer.save()


class MovieViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def perform_create(self, serializer):
        serializer.save()
