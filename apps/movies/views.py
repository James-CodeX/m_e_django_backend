from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, Prefetch
from utils.permissions import IsAdminOrReadOnly
import logging

from .models import (
    Movie, Genre, ProductionCompany, Person,
    MovieCast, MovieCrew
)
from .serializers import (
    MovieListSerializer, MovieDetailSerializer, MovieCreateUpdateSerializer,
    GenreSerializer, GenreDetailSerializer,
    ProductionCompanySerializer, ProductionCompanyDetailSerializer,
    PersonSerializer, PersonDetailSerializer,
    MovieCastSerializer, MovieCrewSerializer
)
from .filters import MovieFilter, GenreFilter, ProductionCompanyFilter, PersonFilter
from .services import MovieSearchService, MovieDataService, TMDBService

logger = logging.getLogger(__name__)


class MovieViewSet(viewsets.ModelViewSet):
    """ViewSet for Movie model"""
    queryset = Movie.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = MovieFilter
    search_fields = ['title', 'original_title', 'overview', 'tagline']
    ordering_fields = [
        'title', 'release_date', 'popularity_score', 'vote_average',
        'vote_count', 'created_at', 'runtime'
    ]
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer class based on action"""
        if self.action == 'list':
            return MovieListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return MovieCreateUpdateSerializer
        return MovieDetailSerializer

    def get_queryset(self):
        """Optimize queryset with select_related and prefetch_related"""
        queryset = Movie.objects.all()
        
        if self.action == 'list':
            queryset = queryset.select_related().prefetch_related(
                'genres',
                'production_companies'
            )
        elif self.action == 'retrieve':
            queryset = queryset.select_related().prefetch_related(
                'genres',
                'production_companies',
                Prefetch(
                    'moviecast_set',
                    queryset=MovieCast.objects.select_related('person').order_by('cast_order')
                ),
                Prefetch(
                    'moviecrew_set',
                    queryset=MovieCrew.objects.select_related('person').order_by('department', 'job')
                )
            )
        
        return queryset

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Enhanced search movies endpoint with TMDB integration"""
        query = request.query_params.get('q', '')
        if not query:
            return Response({'detail': 'Search query parameter "q" is required.'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        # Get search options
        include_tmdb = request.query_params.get('include_tmdb', 'true').lower() == 'true'
        sync_missing = request.query_params.get('sync_missing', 'true').lower() == 'true'
        
        try:
            if include_tmdb and sync_missing:
                # Use comprehensive search that includes TMDB and syncing
                search_service = MovieSearchService()
                search_results = search_service.comprehensive_search(query, include_tmdb=True)
                
                # Combine local and synced results
                all_movies = list(search_results['local_results']) + search_results['synced_movies']
                
                # Serialize the movies
                serializer = MovieListSerializer(all_movies, many=True)
                
                response_data = {
                    'query': query,
                    'results': serializer.data,
                    'search_stats': {
                        'local_count': len(search_results['local_results']),
                        'tmdb_count': len(search_results['tmdb_results']),
                        'synced_count': len(search_results['synced_movies']),
                        'total_count': len(all_movies)
                    }
                }
                
                return Response(response_data)
            else:
                # Standard local search only
                queryset = self.get_queryset().filter(
                    Q(title__icontains=query) |
                    Q(original_title__icontains=query) |
                    Q(overview__icontains=query) |
                    Q(tagline__icontains=query)
                ).distinct()
                
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer = MovieListSerializer(page, many=True)
                    return self.get_paginated_response(serializer.data)
                
                serializer = MovieListSerializer(queryset, many=True)
                return Response({
                    'query': query,
                    'results': serializer.data,
                    'search_stats': {
                        'local_count': len(serializer.data),
                        'tmdb_count': 0,
                        'synced_count': 0,
                        'total_count': len(serializer.data)
                    }
                })
                
        except Exception as e:
            logger.error(f"Search error for query '{query}': {str(e)}")
            return Response(
                {'detail': f'Search failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured movies"""
        queryset = self.get_queryset().filter(is_featured=True)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MovieListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MovieListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get popular movies sorted by popularity score"""
        queryset = self.get_queryset().filter(
            popularity_score__isnull=False
        ).order_by('-popularity_score')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MovieListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MovieListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_rated(self, request):
        """Get top-rated movies sorted by vote average"""
        queryset = self.get_queryset().filter(
            vote_average__isnull=False,
            vote_count__gte=100  # Minimum vote count for reliability
        ).order_by('-vote_average')
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MovieListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MovieListSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """Custom create logic"""
        serializer.save()

    def perform_update(self, serializer):
        """Custom update logic"""
        serializer.save()
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def sync_from_tmdb(self, request):
        """Sync a specific movie from TMDB by ID"""
        tmdb_id = request.data.get('tmdb_id')
        if not tmdb_id:
            return Response(
                {'detail': 'TMDB ID is required.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            movie_service = MovieDataService()
            movie = movie_service.sync_movie_from_tmdb(tmdb_id)
            
            if movie:
                serializer = MovieDetailSerializer(movie)
                return Response({
                    'message': f'Successfully synced movie: {movie.title}',
                    'movie': serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(
                    {'detail': f'Failed to sync movie with TMDB ID: {tmdb_id}'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            logger.error(f"TMDB sync error for ID {tmdb_id}: {str(e)}")
            return Response(
                {'detail': f'Sync failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def sync_genres_from_tmdb(self, request):
        """Sync all genres from TMDB"""
        try:
            movie_service = MovieDataService()
            genres = movie_service.sync_genres_from_tmdb()
            
            serializer = GenreSerializer(genres, many=True)
            return Response({
                'message': f'Successfully synced {len(genres)} genres from TMDB',
                'genres': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"TMDB genre sync error: {str(e)}")
            return Response(
                {'detail': f'Genre sync failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def tmdb_search(self, request):
        """Search TMDB directly without syncing to database"""
        query = request.query_params.get('q', '')
        if not query:
            return Response({'detail': 'Search query parameter "q" is required.'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            tmdb_service = TMDBService()
            results = tmdb_service.search_movies(query)
            
            if results:
                return Response({
                    'query': query,
                    'tmdb_results': results
                })
            else:
                return Response(
                    {'detail': 'No results found on TMDB'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except Exception as e:
            logger.error(f"TMDB search error for query '{query}': {str(e)}")
            return Response(
                {'detail': f'TMDB search failed: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet for Genre model"""
    queryset = Genre.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = GenreFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        """Return appropriate serializer class based on action"""
        if self.action == 'retrieve':
            return GenreDetailSerializer
        return GenreSerializer


class ProductionCompanyViewSet(viewsets.ModelViewSet):
    """ViewSet for ProductionCompany model"""
    queryset = ProductionCompany.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductionCompanyFilter
    search_fields = ['name']
    ordering_fields = ['name', 'origin_country', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        """Return appropriate serializer class based on action"""
        if self.action == 'retrieve':
            return ProductionCompanyDetailSerializer
        return ProductionCompanySerializer


class PersonViewSet(viewsets.ModelViewSet):
    """ViewSet for Person model"""
    queryset = Person.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = PersonFilter
    search_fields = ['name', 'biography', 'place_of_birth']
    ordering_fields = ['name', 'birthday', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        """Return appropriate serializer class based on action"""
        if self.action == 'retrieve':
            return PersonDetailSerializer
        return PersonSerializer
