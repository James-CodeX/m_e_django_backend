import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


class Genre(models.Model):
    """Movie genre model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'genres'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

    @property
    def movie_count(self):
        return self.moviegenre_set.count()


class ProductionCompany(models.Model):
    """Production company model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    logo_url = models.URLField(blank=True)
    origin_country = models.CharField(max_length=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'production_companies'
        ordering = ['name']
        verbose_name_plural = 'Production Companies'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['origin_country']),
        ]

    def __str__(self):
        return self.name

    @property
    def movie_count(self):
        return self.movieproductioncompany_set.count()


class Person(models.Model):
    """Person model for cast and crew"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    biography = models.TextField(blank=True)
    birthday = models.DateField(null=True, blank=True)
    deathday = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(max_length=200, blank=True)
    profile_image_url = models.URLField(blank=True)
    imdb_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'people'
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['imdb_id']),
            models.Index(fields=['tmdb_id']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('movies:person-detail', kwargs={'pk': self.pk})


class Movie(models.Model):
    """Movie model"""
    STATUS_CHOICES = [
        ('released', 'Released'),
        ('upcoming', 'Upcoming'),
        ('in_production', 'In Production'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    original_title = models.CharField(max_length=200, blank=True)
    release_date = models.DateField(null=True, blank=True)
    runtime = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(1)],
        help_text="Runtime in minutes"
    )
    budget = models.BigIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0)]
    )
    revenue = models.BigIntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0)]
    )
    overview = models.TextField(blank=True)
    tagline = models.CharField(max_length=500, blank=True)
    poster_url = models.URLField(blank=True)
    backdrop_url = models.URLField(blank=True)
    trailer_url = models.URLField(blank=True)
    imdb_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='released')
    adult = models.BooleanField(default=False)
    popularity_score = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0)]
    )
    vote_average = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)]
    )
    vote_count = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0)]
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Many-to-many relationships
    genres = models.ManyToManyField(Genre, through='MovieGenre', blank=True)
    production_companies = models.ManyToManyField(
        ProductionCompany, 
        through='MovieProductionCompany', 
        blank=True
    )
    cast = models.ManyToManyField(
        Person, 
        through='MovieCast', 
        related_name='movies_as_cast',
        blank=True
    )
    crew = models.ManyToManyField(
        Person, 
        through='MovieCrew', 
        related_name='movies_as_crew',
        blank=True
    )

    class Meta:
        db_table = 'movies'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['original_title']),
            models.Index(fields=['release_date']),
            models.Index(fields=['status']),
            models.Index(fields=['imdb_id']),
            models.Index(fields=['tmdb_id']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['popularity_score']),
            models.Index(fields=['vote_average']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movies:movie-detail', kwargs={'pk': self.pk})

    @property
    def release_year(self):
        """Get release year from release_date"""
        return self.release_date.year if self.release_date else None

    @property
    def genre_list(self):
        """Get list of genre names"""
        return [genre.name for genre in self.genres.all()]

    @property
    def director(self):
        """Get the director of the movie"""
        director_crew = self.moviecrew_set.filter(job='Director').first()
        return director_crew.person if director_crew else None

    @property
    def main_cast(self):
        """Get main cast members (ordered by cast_order)"""
        return self.moviecast_set.select_related('person').order_by('cast_order')[:10]


class MovieGenre(models.Model):
    """Through model for Movie-Genre relationship"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'movie_genres'
        unique_together = ['movie', 'genre']
        indexes = [
            models.Index(fields=['movie']),
            models.Index(fields=['genre']),
        ]

    def __str__(self):
        return f"{self.movie.title} - {self.genre.name}"


class MovieProductionCompany(models.Model):
    """Through model for Movie-ProductionCompany relationship"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    company = models.ForeignKey(ProductionCompany, on_delete=models.CASCADE)

    class Meta:
        db_table = 'movie_production_companies'
        unique_together = ['movie', 'company']
        indexes = [
            models.Index(fields=['movie']),
            models.Index(fields=['company']),
        ]

    def __str__(self):
        return f"{self.movie.title} - {self.company.name}"


class MovieCast(models.Model):
    """Through model for Movie-Person cast relationship"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    character_name = models.CharField(max_length=200, blank=True)
    cast_order = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'movie_cast'
        unique_together = ['movie', 'person']
        ordering = ['cast_order']
        indexes = [
            models.Index(fields=['movie']),
            models.Index(fields=['person']),
            models.Index(fields=['cast_order']),
        ]

    def __str__(self):
        character = f" as {self.character_name}" if self.character_name else ""
        return f"{self.person.name} in {self.movie.title}{character}"


class MovieCrew(models.Model):
    """Through model for Movie-Person crew relationship"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    job = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'movie_crew'
        unique_together = ['movie', 'person', 'job']
        ordering = ['department', 'job']
        indexes = [
            models.Index(fields=['movie']),
            models.Index(fields=['person']),
            models.Index(fields=['job']),
            models.Index(fields=['department']),
        ]

    def __str__(self):
        return f"{self.person.name} - {self.job} on {self.movie.title}"
