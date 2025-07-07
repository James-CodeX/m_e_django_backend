import django_filters
from django.db.models import Q
from .models import Movie, Genre, ProductionCompany, Person


class MovieFilter(django_filters.FilterSet):
    """Filter for Movie model"""
    
    # Text search
    search = django_filters.CharFilter(method='filter_search')
    
    # Genre filtering
    genre = django_filters.CharFilter(method='filter_genre')
    genre_id = django_filters.UUIDFilter(field_name='genres__id')
    
    # Year filtering
    year = django_filters.NumberFilter(method='filter_year')
    year_gte = django_filters.NumberFilter(field_name='release_date__year', lookup_expr='gte')
    year_lte = django_filters.NumberFilter(field_name='release_date__year', lookup_expr='lte')
    
    # Status filtering
    status = django_filters.ChoiceFilter(choices=Movie.STATUS_CHOICES)
    
    # Rating filtering
    rating_gte = django_filters.NumberFilter(field_name='vote_average', lookup_expr='gte')
    rating_lte = django_filters.NumberFilter(field_name='vote_average', lookup_expr='lte')
    
    # Popularity filtering
    popularity_gte = django_filters.NumberFilter(field_name='popularity_score', lookup_expr='gte')
    popularity_lte = django_filters.NumberFilter(field_name='popularity_score', lookup_expr='lte')
    
    # Featured movies
    featured = django_filters.BooleanFilter(field_name='is_featured')
    
    # Adult content
    adult = django_filters.BooleanFilter(field_name='adult')
    
    # Production company
    production_company = django_filters.CharFilter(method='filter_production_company')
    production_company_id = django_filters.UUIDFilter(field_name='production_companies__id')
    
    # Runtime filtering
    runtime_gte = django_filters.NumberFilter(field_name='runtime', lookup_expr='gte')
    runtime_lte = django_filters.NumberFilter(field_name='runtime', lookup_expr='lte')
    
    # Release date filtering
    release_date_gte = django_filters.DateFilter(field_name='release_date', lookup_expr='gte')
    release_date_lte = django_filters.DateFilter(field_name='release_date', lookup_expr='lte')

    class Meta:
        model = Movie
        fields = {
            'title': ['icontains'],
            'original_title': ['icontains'],
            'imdb_id': ['exact'],
            'tmdb_id': ['exact'],
        }

    def filter_search(self, queryset, name, value):
        """Search across multiple fields"""
        if value:
            return queryset.filter(
                Q(title__icontains=value) |
                Q(original_title__icontains=value) |
                Q(overview__icontains=value) |
                Q(tagline__icontains=value)
            ).distinct()
        return queryset

    def filter_genre(self, queryset, name, value):
        """Filter by genre name"""
        if value:
            return queryset.filter(genres__name__icontains=value).distinct()
        return queryset

    def filter_year(self, queryset, name, value):
        """Filter by release year"""
        if value:
            return queryset.filter(release_date__year=value)
        return queryset

    def filter_production_company(self, queryset, name, value):
        """Filter by production company name"""
        if value:
            return queryset.filter(production_companies__name__icontains=value).distinct()
        return queryset


class GenreFilter(django_filters.FilterSet):
    """Filter for Genre model"""
    search = django_filters.CharFilter(method='filter_search')
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Genre
        fields = ['name']

    def filter_search(self, queryset, name, value):
        """Search across genre fields"""
        if value:
            return queryset.filter(
                Q(name__icontains=value) |
                Q(description__icontains=value)
            ).distinct()
        return queryset


class ProductionCompanyFilter(django_filters.FilterSet):
    """Filter for ProductionCompany model"""
    search = django_filters.CharFilter(method='filter_search')
    name = django_filters.CharFilter(lookup_expr='icontains')
    origin_country = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = ProductionCompany
        fields = ['name', 'origin_country']

    def filter_search(self, queryset, name, value):
        """Search across production company fields"""
        if value:
            return queryset.filter(
                Q(name__icontains=value)
            ).distinct()
        return queryset


class PersonFilter(django_filters.FilterSet):
    """Filter for Person model"""
    search = django_filters.CharFilter(method='filter_search')
    name = django_filters.CharFilter(lookup_expr='icontains')
    place_of_birth = django_filters.CharFilter(lookup_expr='icontains')
    
    # Age filtering (alive people)
    birth_year_gte = django_filters.NumberFilter(field_name='birthday__year', lookup_expr='gte')
    birth_year_lte = django_filters.NumberFilter(field_name='birthday__year', lookup_expr='lte')
    
    # Filter by alive/deceased
    is_alive = django_filters.BooleanFilter(method='filter_is_alive')

    class Meta:
        model = Person
        fields = {
            'imdb_id': ['exact'],
            'tmdb_id': ['exact'],
        }

    def filter_search(self, queryset, name, value):
        """Search across person fields"""
        if value:
            return queryset.filter(
                Q(name__icontains=value) |
                Q(biography__icontains=value) |
                Q(place_of_birth__icontains=value)
            ).distinct()
        return queryset

    def filter_is_alive(self, queryset, name, value):
        """Filter by whether person is alive or deceased"""
        if value is True:
            return queryset.filter(deathday__isnull=True)
        elif value is False:
            return queryset.filter(deathday__isnull=False)
        return queryset
