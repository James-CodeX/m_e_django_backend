"""
Services for external API integrations and business logic for movies app.
This file contains TMDB API integration and movie data synchronization services.
"""

import requests
import logging
from datetime import datetime
from django.conf import settings
from django.db import transaction
from typing import Dict, List, Optional, Union

from .models import (
    Movie, Genre, ProductionCompany, Person,
    MovieGenre, MovieProductionCompany, MovieCast, MovieCrew
)

logger = logging.getLogger(__name__)


class TMDBService:
    """Service for TMDB API integration"""
    
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.access_token = settings.TMDB_ACCESS_TOKEN
        self.base_url = settings.TMDB_BASE_URL
        self.image_base_url = settings.TMDB_IMAGE_BASE_URL
        self.image_sizes = settings.TMDB_IMAGE_SIZES
        
        # Request headers for API v4 (using access token)
        self.headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json;charset=utf-8'
        }
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Optional[Dict]:
        """Make a request to TMDB API"""
        url = f"{self.base_url}/{endpoint}"
        
        # Add API key to params if not using access token
        if params is None:
            params = {}
        params['api_key'] = self.api_key
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"TMDB API request failed: {e}")
            return None
    
    def _build_image_url(self, path: str, size_type: str = 'poster') -> str:
        """Build full image URL from TMDB path"""
        if not path:
            return ''
        size = self.image_sizes.get(size_type, 'w500')
        return f"{self.image_base_url}/{size}{path}"
    
    def search_movies(self, query: str, page: int = 1) -> Optional[Dict]:
        """Search movies on TMDB"""
        endpoint = 'search/movie'
        params = {
            'query': query,
            'page': page,
            'include_adult': False,
            'language': 'en-US'
        }
        return self._make_request(endpoint, params)
    
    def fetch_movie_data(self, tmdb_id: int) -> Optional[Dict]:
        """Fetch detailed movie data from TMDB API"""
        endpoint = f'movie/{tmdb_id}'
        params = {
            'append_to_response': 'credits,videos,keywords,external_ids',
            'language': 'en-US'
        }
        return self._make_request(endpoint, params)
    
    def fetch_person_data(self, tmdb_id: int) -> Optional[Dict]:
        """Fetch person data from TMDB API"""
        endpoint = f'person/{tmdb_id}'
        params = {
            'append_to_response': 'movie_credits,external_ids',
            'language': 'en-US'
        }
        return self._make_request(endpoint, params)
    
    def fetch_genre_list(self) -> Optional[Dict]:
        """Fetch genre list from TMDB"""
        endpoint = 'genre/movie/list'
        params = {'language': 'en-US'}
        return self._make_request(endpoint, params)
    
    def fetch_production_company(self, company_id: int) -> Optional[Dict]:
        """Fetch production company data from TMDB"""
        endpoint = f'company/{company_id}'
        return self._make_request(endpoint)


class MovieDataService:
    """Service for movie data management and TMDB synchronization"""
    
    def __init__(self):
        self.tmdb_service = TMDBService()
    
    def _parse_date(self, date_string: str) -> Optional[datetime]:
        """Parse date string from TMDB API"""
        if not date_string:
            return None
        try:
            return datetime.strptime(date_string, '%Y-%m-%d').date()
        except ValueError:
            logger.warning(f"Failed to parse date: {date_string}")
            return None
    
    def _get_or_create_genre(self, genre_data: Dict) -> Genre:
        """Get or create genre from TMDB data"""
        genre, created = Genre.objects.get_or_create(
            name=genre_data['name'],
            defaults={
                'description': f"Genre: {genre_data['name']}"
            }
        )
        if created:
            logger.info(f"Created new genre: {genre.name}")
        return genre
    
    def _get_or_create_production_company(self, company_data: Dict) -> ProductionCompany:
        """Get or create production company from TMDB data"""
        # Fetch additional company data if needed
        if 'logo_path' not in company_data and company_data.get('id'):
            additional_data = self.tmdb_service.fetch_production_company(company_data['id'])
            if additional_data:
                company_data.update(additional_data)
        
        company, created = ProductionCompany.objects.get_or_create(
            name=company_data['name'],
            defaults={
                'logo_url': self.tmdb_service._build_image_url(
                    company_data.get('logo_path', ''), 'poster'
                ) if company_data.get('logo_path') else '',
                'origin_country': company_data.get('origin_country', '')
            }
        )
        if created:
            logger.info(f"Created new production company: {company.name}")
        return company
    
    def _get_or_create_person(self, person_data: Dict) -> Person:
        """Get or create person from TMDB data"""
        person, created = Person.objects.get_or_create(
            tmdb_id=person_data['id'],
            defaults={
                'name': person_data['name'],
                'profile_image_url': self.tmdb_service._build_image_url(
                    person_data.get('profile_path', ''), 'profile'
                ) if person_data.get('profile_path') else ''
            }
        )
        if created:
            logger.info(f"Created new person: {person.name}")
        return person
    
    @transaction.atomic
    def sync_movie_from_tmdb(self, tmdb_id: int) -> Optional[Movie]:
        """Sync movie data from TMDB and create/update database record"""
        logger.info(f"Syncing movie with TMDB ID: {tmdb_id}")
        
        # Check if movie already exists
        existing_movie = Movie.objects.filter(tmdb_id=tmdb_id).first()
        if existing_movie:
            logger.info(f"Movie already exists: {existing_movie.title}")
            return existing_movie
        
        # Fetch movie data from TMDB
        movie_data = self.tmdb_service.fetch_movie_data(tmdb_id)
        if not movie_data:
            logger.error(f"Failed to fetch movie data for TMDB ID: {tmdb_id}")
            return None
        
        try:
            # Create movie object
            movie = Movie.objects.create(
                tmdb_id=tmdb_id,
                title=movie_data.get('title', ''),
                original_title=movie_data.get('original_title', ''),
                overview=movie_data.get('overview', ''),
                tagline=movie_data.get('tagline', ''),
                release_date=self._parse_date(movie_data.get('release_date')),
                runtime=movie_data.get('runtime'),
                budget=movie_data.get('budget', 0) if movie_data.get('budget') else None,
                revenue=movie_data.get('revenue', 0) if movie_data.get('revenue') else None,
                status=self._map_tmdb_status(movie_data.get('status', 'Released')),
                adult=movie_data.get('adult', False),
                popularity_score=movie_data.get('popularity'),
                vote_average=movie_data.get('vote_average'),
                vote_count=movie_data.get('vote_count'),
                poster_url=self.tmdb_service._build_image_url(
                    movie_data.get('poster_path', ''), 'poster'
                ) if movie_data.get('poster_path') else '',
                backdrop_url=self.tmdb_service._build_image_url(
                    movie_data.get('backdrop_path', ''), 'backdrop'
                ) if movie_data.get('backdrop_path') else '',
                imdb_id=movie_data.get('external_ids', {}).get('imdb_id') if movie_data.get('external_ids') else None
            )
            
            # Add genres
            if movie_data.get('genres'):
                for genre_data in movie_data['genres']:
                    genre = self._get_or_create_genre(genre_data)
                    MovieGenre.objects.create(movie=movie, genre=genre)
            
            # Add production companies
            if movie_data.get('production_companies'):
                for company_data in movie_data['production_companies']:
                    company = self._get_or_create_production_company(company_data)
                    MovieProductionCompany.objects.create(movie=movie, company=company)
            
            # Add cast and crew if available
            credits = movie_data.get('credits', {})
            
            # Add cast
            if credits.get('cast'):
                for i, cast_data in enumerate(credits['cast'][:20]):  # Limit to top 20 cast
                    person = self._get_or_create_person(cast_data)
                    MovieCast.objects.create(
                        movie=movie,
                        person=person,
                        character_name=cast_data.get('character', ''),
                        cast_order=cast_data.get('order', i)
                    )
            
            # Add crew
            if credits.get('crew'):
                # Focus on key crew members (Director, Producer, Writer, etc.)
                key_jobs = ['Director', 'Producer', 'Executive Producer', 'Screenplay', 'Writer', 
                           'Director of Photography', 'Original Music Composer', 'Editor']
                for crew_data in credits['crew']:
                    if crew_data.get('job') in key_jobs:
                        person = self._get_or_create_person(crew_data)
                        MovieCrew.objects.create(
                            movie=movie,
                            person=person,
                            job=crew_data.get('job', ''),
                            department=crew_data.get('department', '')
                        )
            
            logger.info(f"Successfully synced movie: {movie.title}")
            return movie
            
        except Exception as e:
            logger.error(f"Error syncing movie {tmdb_id}: {str(e)}")
            return None
    
    def _map_tmdb_status(self, tmdb_status: str) -> str:
        """Map TMDB status to our model choices"""
        status_mapping = {
            'Released': 'released',
            'Post Production': 'upcoming',
            'In Production': 'in_production',
            'Planned': 'upcoming',
            'Rumored': 'upcoming',
            'Canceled': 'released'  # Default to released for canceled movies
        }
        return status_mapping.get(tmdb_status, 'released')
    
    def search_and_sync_movies(self, query: str, max_results: int = 10) -> List[Movie]:
        """Search TMDB and sync movies to local database"""
        logger.info(f"Searching and syncing movies for query: {query}")
        
        search_results = self.tmdb_service.search_movies(query)
        if not search_results or not search_results.get('results'):
            logger.warning(f"No search results found for query: {query}")
            return []
        
        synced_movies = []
        for movie_data in search_results['results'][:max_results]:
            tmdb_id = movie_data.get('id')
            if tmdb_id:
                # Check if already exists
                existing_movie = Movie.objects.filter(tmdb_id=tmdb_id).first()
                if existing_movie:
                    synced_movies.append(existing_movie)
                else:
                    synced_movie = self.sync_movie_from_tmdb(tmdb_id)
                    if synced_movie:
                        synced_movies.append(synced_movie)
        
        logger.info(f"Synced {len(synced_movies)} movies for query: {query}")
        return synced_movies
    
    def sync_genres_from_tmdb(self) -> List[Genre]:
        """Sync genre list from TMDB"""
        logger.info("Syncing genres from TMDB")
        
        genre_data = self.tmdb_service.fetch_genre_list()
        if not genre_data or not genre_data.get('genres'):
            logger.warning("No genres found in TMDB response")
            return []
        
        synced_genres = []
        for genre_info in genre_data['genres']:
            genre = self._get_or_create_genre(genre_info)
            synced_genres.append(genre)
        
        logger.info(f"Synced {len(synced_genres)} genres from TMDB")
        return synced_genres
    
    @staticmethod
    def update_movie_ratings():
        """Update movie ratings from external sources"""
        # TODO: Implement rating update logic for existing movies
        logger.info("Movie ratings update not yet implemented")
        pass
    
    @staticmethod
    def generate_movie_recommendations(movie_id):
        """Generate movie recommendations"""
        # TODO: Implement recommendation generation logic
        logger.info(f"Movie recommendations generation for {movie_id} not yet implemented")
        pass


class MovieSearchService:
    """Service for enhanced movie search functionality"""
    
    def __init__(self):
        self.movie_data_service = MovieDataService()
        self.tmdb_service = TMDBService()
    
    def comprehensive_search(self, query: str, include_tmdb: bool = True) -> Dict:
        """Perform comprehensive movie search combining local and TMDB data"""
        logger.info(f"Performing comprehensive search for: {query}")
        
        # Search local database first
        from django.db.models import Q
        local_movies = Movie.objects.filter(
            Q(title__icontains=query) |
            Q(original_title__icontains=query) |
            Q(overview__icontains=query)
        ).select_related().prefetch_related('genres', 'production_companies')[:10]
        
        result = {
            'query': query,
            'local_results': list(local_movies),
            'tmdb_results': [],
            'synced_movies': []
        }
        
        # If we have local results and not including TMDB, return early
        if local_movies.exists() and not include_tmdb:
            logger.info(f"Found {local_movies.count()} local results for: {query}")
            return result
        
        # Search TMDB if requested
        if include_tmdb:
            tmdb_results = self.tmdb_service.search_movies(query)
            if tmdb_results and tmdb_results.get('results'):
                result['tmdb_results'] = tmdb_results['results'][:10]
                
                # If no local results, sync some movies from TMDB
                if not local_movies.exists():
                    logger.info(f"No local results found, syncing from TMDB for: {query}")
                    synced_movies = self.movie_data_service.search_and_sync_movies(query, max_results=5)
                    result['synced_movies'] = synced_movies
        
        logger.info(f"Search completed for: {query}. Local: {len(result['local_results'])}, "
                   f"TMDB: {len(result['tmdb_results'])}, Synced: {len(result['synced_movies'])}")
        return result
    
    def get_trending_movies(self) -> List[Movie]:
        """Get trending movies based on popularity and recent additions"""
        # TODO: Implement more sophisticated trending algorithm
        return Movie.objects.filter(
            popularity_score__isnull=False
        ).order_by('-popularity_score', '-created_at')[:20]
    
    def get_recommendations_for_user(self, user_id):
        """Get personalized recommendations for user"""
        # TODO: Implement user-based recommendations when user preferences are available
        logger.info(f"User recommendations for {user_id} not yet implemented")
        return []
    
    def sync_movie_by_tmdb_id(self, tmdb_id: int) -> Optional[Movie]:
        """Direct method to sync a specific movie by TMDB ID"""
        return self.movie_data_service.sync_movie_from_tmdb(tmdb_id)
