from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, GenreViewSet, ProductionCompanyViewSet, PersonViewSet

app_name = 'movies'

# Create router and register viewsets
router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'production-companies', ProductionCompanyViewSet, basename='production-company')
router.register(r'people', PersonViewSet, basename='person')

urlpatterns = [
    path('', include(router.urls)),
]
