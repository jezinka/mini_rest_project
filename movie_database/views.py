from rest_framework import viewsets

from movie_database.models import Genre
from movie_database.serializers import GenreSerializer


class GenreViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def perform_create(self, serializer):
        serializer.save()
