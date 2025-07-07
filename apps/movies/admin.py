from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Movie, Genre, ProductionCompany, Person,
    MovieGenre, MovieProductionCompany, MovieCast, MovieCrew
)


class MovieGenreInline(admin.TabularInline):
    """Inline for movie genres"""
    model = MovieGenre
    extra = 1
    autocomplete_fields = ['genre']


class MovieProductionCompanyInline(admin.TabularInline):
    """Inline for movie production companies"""
    model = MovieProductionCompany
    extra = 1
    autocomplete_fields = ['company']


class MovieCastInline(admin.TabularInline):
    """Inline for movie cast"""
    model = MovieCast
    extra = 1
    autocomplete_fields = ['person']
    fields = ['person', 'character_name', 'cast_order']
    ordering = ['cast_order']


class MovieCrewInline(admin.TabularInline):
    """Inline for movie crew"""
    model = MovieCrew
    extra = 1
    autocomplete_fields = ['person']
    fields = ['person', 'job', 'department']
    ordering = ['department', 'job']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Admin for Genre model"""
    list_display = ['name', 'movie_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at']
    ordering = ['name']

    def movie_count(self, obj):
        return obj.movie_count
    movie_count.short_description = 'Movie Count'


@admin.register(ProductionCompany)
class ProductionCompanyAdmin(admin.ModelAdmin):
    """Admin for ProductionCompany model"""
    list_display = ['name', 'origin_country', 'movie_count', 'created_at']
    list_filter = ['origin_country', 'created_at']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at']
    ordering = ['name']

    def movie_count(self, obj):
        return obj.movie_count
    movie_count.short_description = 'Movie Count'


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    """Admin for Person model"""
    list_display = ['name', 'birthday', 'place_of_birth', 'imdb_link', 'created_at']
    list_filter = ['birthday', 'deathday', 'created_at']
    search_fields = ['name', 'biography', 'place_of_birth']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = [
        ('Basic Information', {
            'fields': ['name', 'biography', 'profile_image_url']
        }),
        ('Birth & Death', {
            'fields': ['birthday', 'deathday', 'place_of_birth']
        }),
        ('External IDs', {
            'fields': ['imdb_id', 'tmdb_id']
        }),
        ('Metadata', {
            'fields': ['id', 'created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    ordering = ['name']

    def imdb_link(self, obj):
        if obj.imdb_id:
            return format_html(
                '<a href="https://www.imdb.com/name/{}" target="_blank">{}</a>',
                obj.imdb_id, obj.imdb_id
            )
        return '-'
    imdb_link.short_description = 'IMDB Link'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Admin for Movie model"""
    list_display = [
        'title', 'release_date', 'status', 'vote_average',
        'popularity_score', 'is_featured', 'imdb_link'
    ]
    list_filter = [
        'status', 'is_featured', 'adult', 'release_date',
        'created_at', 'genres', 'production_companies'
    ]
    search_fields = ['title', 'original_title', 'overview', 'imdb_id', 'tmdb_id']
    readonly_fields = ['id', 'created_at', 'updated_at', 'release_year']
    filter_horizontal = []
    date_hierarchy = 'release_date'
    ordering = ['-created_at']
    
    fieldsets = [
        ('Basic Information', {
            'fields': ['title', 'original_title', 'overview', 'tagline', 'status']
        }),
        ('Release & Runtime', {
            'fields': ['release_date', 'release_year', 'runtime']
        }),
        ('Financial', {
            'fields': ['budget', 'revenue']
        }),
        ('Ratings & Popularity', {
            'fields': ['vote_average', 'vote_count', 'popularity_score']
        }),
        ('Media', {
            'fields': ['poster_url', 'backdrop_url', 'trailer_url']
        }),
        ('External IDs', {
            'fields': ['imdb_id', 'tmdb_id']
        }),
        ('Flags', {
            'fields': ['adult', 'is_featured']
        }),
        ('Metadata', {
            'fields': ['id', 'created_at', 'updated_at'],
            'classes': ['collapse']
        })
    ]
    
    inlines = [
        MovieGenreInline,
        MovieProductionCompanyInline,
        MovieCastInline,
        MovieCrewInline
    ]

    def imdb_link(self, obj):
        if obj.imdb_id:
            return format_html(
                '<a href="https://www.imdb.com/title/{}" target="_blank">{}</a>',
                obj.imdb_id, obj.imdb_id
            )
        return '-'
    imdb_link.short_description = 'IMDB Link'

    def get_queryset(self, request):
        """Optimize queryset for admin"""
        return super().get_queryset(request).select_related().prefetch_related(
            'genres', 'production_companies'
        )


@admin.register(MovieCast)
class MovieCastAdmin(admin.ModelAdmin):
    """Admin for MovieCast model"""
    list_display = ['movie', 'person', 'character_name', 'cast_order']
    list_filter = ['created_at']
    search_fields = ['movie__title', 'person__name', 'character_name']
    autocomplete_fields = ['movie', 'person']
    ordering = ['movie', 'cast_order']


@admin.register(MovieCrew)
class MovieCrewAdmin(admin.ModelAdmin):
    """Admin for MovieCrew model"""
    list_display = ['movie', 'person', 'job', 'department']
    list_filter = ['job', 'department', 'created_at']
    search_fields = ['movie__title', 'person__name', 'job', 'department']
    autocomplete_fields = ['movie', 'person']
    ordering = ['movie', 'department', 'job']
