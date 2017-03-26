from rest_framework import viewsets

from movie_database.models import Genre, OscarAward
from movie_database.serializers import GenreSerializer, OscarAwardSerializer


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
