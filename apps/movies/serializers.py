from rest_framework import serializers
from .models import (
    Movie, Genre, ProductionCompany, Person, 
    MovieGenre, MovieProductionCompany, MovieCast, MovieCrew
)


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre model"""
    movie_count = serializers.ReadOnlyField()

    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'created_at', 'movie_count']
        read_only_fields = ['id', 'created_at', 'movie_count']


class ProductionCompanySerializer(serializers.ModelSerializer):
    """Serializer for ProductionCompany model"""
    movie_count = serializers.ReadOnlyField()

    class Meta:
        model = ProductionCompany
        fields = ['id', 'name', 'logo_url', 'origin_country', 'created_at', 'movie_count']
        read_only_fields = ['id', 'created_at', 'movie_count']


class PersonSerializer(serializers.ModelSerializer):
    """Serializer for Person model"""
    
    class Meta:
        model = Person
        fields = [
            'id', 'name', 'biography', 'birthday', 'deathday', 
            'place_of_birth', 'profile_image_url', 'imdb_id', 
            'tmdb_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class MovieCastSerializer(serializers.ModelSerializer):
    """Serializer for MovieCast model"""
    person = PersonSerializer(read_only=True)
    person_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = MovieCast
        fields = ['id', 'person', 'person_id', 'character_name', 'cast_order', 'created_at']
        read_only_fields = ['id', 'created_at']


class MovieCrewSerializer(serializers.ModelSerializer):
    """Serializer for MovieCrew model"""
    person = PersonSerializer(read_only=True)
    person_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = MovieCrew
        fields = ['id', 'person', 'person_id', 'job', 'department', 'created_at']
        read_only_fields = ['id', 'created_at']


class MovieListSerializer(serializers.ModelSerializer):
    """Serializer for Movie list view (minimal fields)"""
    genres = GenreSerializer(many=True, read_only=True)
    production_companies = ProductionCompanySerializer(many=True, read_only=True)
    release_year = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'original_title', 'release_date', 'release_year',
            'runtime', 'overview', 'tagline', 'poster_url', 'backdrop_url',
            'trailer_url', 'imdb_id', 'tmdb_id', 'status', 'adult',
            'popularity_score', 'vote_average', 'vote_count', 'is_featured',
            'created_at', 'updated_at', 'genres', 'production_companies'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'release_year']


class MovieDetailSerializer(serializers.ModelSerializer):
    """Serializer for Movie detail view (all fields including cast/crew)"""
    genres = GenreSerializer(many=True, read_only=True)
    production_companies = ProductionCompanySerializer(many=True, read_only=True)
    cast = MovieCastSerializer(source='moviecast_set', many=True, read_only=True)
    crew = MovieCrewSerializer(source='moviecrew_set', many=True, read_only=True)
    release_year = serializers.ReadOnlyField()
    director = PersonSerializer(read_only=True)
    genre_list = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'original_title', 'release_date', 'release_year',
            'runtime', 'budget', 'revenue', 'overview', 'tagline', 'poster_url',
            'backdrop_url', 'trailer_url', 'imdb_id', 'tmdb_id', 'status', 'adult',
            'popularity_score', 'vote_average', 'vote_count', 'is_featured',
            'created_at', 'updated_at', 'genres', 'production_companies',
            'cast', 'crew', 'director', 'genre_list'
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at', 'release_year', 
            'director', 'genre_list'
        ]


class MovieCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for Movie create/update operations"""
    genre_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False,
        allow_empty=True
    )
    production_company_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False,
        allow_empty=True
    )

    class Meta:
        model = Movie
        fields = [
            'id', 'title', 'original_title', 'release_date', 'runtime',
            'budget', 'revenue', 'overview', 'tagline', 'poster_url',
            'backdrop_url', 'trailer_url', 'imdb_id', 'tmdb_id', 'status',
            'adult', 'popularity_score', 'vote_average', 'vote_count',
            'is_featured', 'genre_ids', 'production_company_ids'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        genre_ids = validated_data.pop('genre_ids', [])
        production_company_ids = validated_data.pop('production_company_ids', [])
        
        movie = Movie.objects.create(**validated_data)
        
        # Add genres
        if genre_ids:
            for genre_id in genre_ids:
                try:
                    genre = Genre.objects.get(id=genre_id)
                    MovieGenre.objects.create(movie=movie, genre=genre)
                except Genre.DoesNotExist:
                    pass
        
        # Add production companies
        if production_company_ids:
            for company_id in production_company_ids:
                try:
                    company = ProductionCompany.objects.get(id=company_id)
                    MovieProductionCompany.objects.create(movie=movie, company=company)
                except ProductionCompany.DoesNotExist:
                    pass
        
        return movie

    def update(self, instance, validated_data):
        genre_ids = validated_data.pop('genre_ids', None)
        production_company_ids = validated_data.pop('production_company_ids', None)
        
        # Update movie fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update genres if provided
        if genre_ids is not None:
            instance.moviegenre_set.all().delete()
            for genre_id in genre_ids:
                try:
                    genre = Genre.objects.get(id=genre_id)
                    MovieGenre.objects.create(movie=instance, genre=genre)
                except Genre.DoesNotExist:
                    pass
        
        # Update production companies if provided
        if production_company_ids is not None:
            instance.movieproductioncompany_set.all().delete()
            for company_id in production_company_ids:
                try:
                    company = ProductionCompany.objects.get(id=company_id)
                    MovieProductionCompany.objects.create(movie=instance, company=company)
                except ProductionCompany.DoesNotExist:
                    pass
        
        return instance


class GenreDetailSerializer(serializers.ModelSerializer):
    """Serializer for Genre detail view with movies"""
    movies = MovieListSerializer(source='moviegenre_set.movie', many=True, read_only=True)

    class Meta:
        model = Genre
        fields = ['id', 'name', 'description', 'created_at', 'movies']
        read_only_fields = ['id', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Get movies through the relationship
        movies = Movie.objects.filter(moviegenre__genre=instance).select_related()
        movie_data = []
        for movie in movies:
            movie_data.append({
                'id': movie.id,
                'title': movie.title,
                'release_date': movie.release_date,
                'poster_url': movie.poster_url,
                'vote_average': movie.vote_average,
                'popularity_score': movie.popularity_score
            })
        data['movies'] = movie_data
        return data


class ProductionCompanyDetailSerializer(serializers.ModelSerializer):
    """Serializer for ProductionCompany detail view with movies"""
    movies = MovieListSerializer(source='movieproductioncompany_set.movie', many=True, read_only=True)

    class Meta:
        model = ProductionCompany
        fields = ['id', 'name', 'logo_url', 'origin_country', 'created_at', 'movies']
        read_only_fields = ['id', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Get movies through the relationship
        movies = Movie.objects.filter(movieproductioncompany__company=instance).select_related()
        movie_data = []
        for movie in movies:
            movie_data.append({
                'id': movie.id,
                'title': movie.title,
                'release_date': movie.release_date,
                'poster_url': movie.poster_url,
                'vote_average': movie.vote_average,
                'popularity_score': movie.popularity_score
            })
        data['movies'] = movie_data
        return data


class PersonDetailSerializer(serializers.ModelSerializer):
    """Serializer for Person detail view with filmography"""
    cast_roles = serializers.SerializerMethodField()
    crew_roles = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = [
            'id', 'name', 'biography', 'birthday', 'deathday',
            'place_of_birth', 'profile_image_url', 'imdb_id',
            'tmdb_id', 'created_at', 'updated_at', 'cast_roles', 'crew_roles'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_cast_roles(self, obj):
        cast_roles = MovieCast.objects.filter(person=obj).select_related('movie')
        return [
            {
                'movie': {
                    'id': role.movie.id,
                    'title': role.movie.title,
                    'release_date': role.movie.release_date,
                    'poster_url': role.movie.poster_url
                },
                'character_name': role.character_name,
                'cast_order': role.cast_order
            }
            for role in cast_roles
        ]

    def get_crew_roles(self, obj):
        crew_roles = MovieCrew.objects.filter(person=obj).select_related('movie')
        return [
            {
                'movie': {
                    'id': role.movie.id,
                    'title': role.movie.title,
                    'release_date': role.movie.release_date,
                    'poster_url': role.movie.poster_url
                },
                'job': role.job,
                'department': role.department
            }
            for role in crew_roles
        ]
