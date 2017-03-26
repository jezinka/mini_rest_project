from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from movie_database import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'genres', views.GenreViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
