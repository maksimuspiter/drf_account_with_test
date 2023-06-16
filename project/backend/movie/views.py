from movie.serializers import MovieSerializer, ResourceSerializer
from movie.models import Movie, Resource
from rest_framework import viewsets


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    permission_classes = []
    serializer_class = MovieSerializer


class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    permission_classes = []
    serializer_class = ResourceSerializer
