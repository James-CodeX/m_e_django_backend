# Stage 2: Movies App Implementation

## Overview
This document details the implementation of Stage 2 (3.2.2 Movies App) of the MovieExplained backend project.

## Models Implemented

### 1. Movie Model
**Table:** `movies`
**Fields:**
- `id` (UUID, Primary Key)
- `title` (CharField, max_length=200, Required)
- `original_title` (CharField, max_length=200, Optional)
- `release_date` (DateField, Optional)
- `runtime` (IntegerField, Optional) - minutes
- `budget` (BigIntegerField, Optional)
- `revenue` (BigIntegerField, Optional)
- `overview` (TextField, Optional)
- `tagline` (CharField, max_length=500, Optional)
- `poster_url` (URLField, Optional)
- `backdrop_url` (URLField, Optional)
- `trailer_url` (URLField, Optional)
- `imdb_id` (CharField, max_length=20, Unique, Optional)
- `tmdb_id` (IntegerField, Unique, Optional)
- `status` (CharField, choices: released, upcoming, in_production)
- `adult` (BooleanField, default=False)
- `popularity_score` (FloatField, Optional)
- `vote_average` (FloatField, Optional)
- `vote_count` (IntegerField, Optional)
- `created_at` (DateTimeField, auto_now_add=True)
- `updated_at` (DateTimeField, auto_now=True)
- `is_featured` (BooleanField, default=False)

### 2. Genre Model
**Table:** `genres`
**Fields:**
- `id` (UUID, Primary Key)
- `name` (CharField, max_length=50, Unique)
- `description` (TextField, Optional)
- `created_at` (DateTimeField, auto_now_add=True)

### 3. MovieGenre Model (Many-to-Many Relationship)
**Table:** `movie_genres`
**Fields:**
- `id` (UUID, Primary Key)
- `movie` (ForeignKey to Movie)
- `genre` (ForeignKey to Genre)
- `created_at` (DateTimeField, auto_now_add=True)

### 4. ProductionCompany Model
**Table:** `production_companies`
**Fields:**
- `id` (UUID, Primary Key)
- `name` (CharField, max_length=100, Unique)
- `logo_url` (URLField, Optional)
- `origin_country` (CharField, max_length=2, Optional)
- `created_at` (DateTimeField, auto_now_add=True)

### 5. MovieProductionCompany Model (Many-to-Many Relationship)
**Table:** `movie_production_companies`
**Fields:**
- `id` (UUID, Primary Key)
- `movie` (ForeignKey to Movie)
- `company` (ForeignKey to ProductionCompany)

### 6. Person Model
**Table:** `people`
**Fields:**
- `id` (UUID, Primary Key)
- `name` (CharField, max_length=100, Required)
- `biography` (TextField, Optional)
- `birthday` (DateField, Optional)
- `deathday` (DateField, Optional)
- `place_of_birth` (CharField, max_length=200, Optional)
- `profile_image_url` (URLField, Optional)
- `imdb_id` (CharField, max_length=20, Unique, Optional)
- `tmdb_id` (IntegerField, Unique, Optional)
- `created_at` (DateTimeField, auto_now_add=True)
- `updated_at` (DateTimeField, auto_now=True)

### 7. MovieCast Model
**Table:** `movie_cast`
**Fields:**
- `id` (UUID, Primary Key)
- `movie` (ForeignKey to Movie)
- `person` (ForeignKey to Person)
- `character_name` (CharField, max_length=200, Optional)
- `cast_order` (IntegerField, Optional)
- `created_at` (DateTimeField, auto_now_add=True)

### 8. MovieCrew Model
**Table:** `movie_crew`
**Fields:**
- `id` (UUID, Primary Key)
- `movie` (ForeignKey to Movie)
- `person` (ForeignKey to Person)
- `job` (CharField, max_length=100, Optional)
- `department` (CharField, max_length=50, Optional)
- `created_at` (DateTimeField, auto_now_add=True)

## API Endpoints

### Public Movie Endpoints (No Authentication Required)

#### 1. List Movies
- **URL:** `GET /api/v1/movies/`
- **Permission:** AllowAny
- **Description:** List all movies with pagination and filters
- **Query Parameters:**
  - `page` (int, optional) - Page number
  - `search` (string, optional) - Search in title, original_title, overview
  - `genre` (string, optional) - Filter by genre name
  - `year` (int, optional) - Filter by release year
  - `status` (string, optional) - Filter by status
  - `featured` (bool, optional) - Filter featured movies
  - `ordering` (string, optional) - Order by fields (title, release_date, popularity_score, vote_average)

**Response Fields:**
```json
{
  "count": "integer",
  "next": "string (url)",
  "previous": "string (url)",
  "results": [
    {
      "id": "uuid",
      "title": "string",
      "original_title": "string",
      "release_date": "date",
      "runtime": "integer",
      "budget": "integer",
      "revenue": "integer",
      "overview": "string",
      "tagline": "string",
      "poster_url": "string",
      "backdrop_url": "string",
      "trailer_url": "string",
      "imdb_id": "string",
      "tmdb_id": "integer",
      "status": "string",
      "adult": "boolean",
      "popularity_score": "float",
      "vote_average": "float",
      "vote_count": "integer",
      "is_featured": "boolean",
      "created_at": "datetime",
      "updated_at": "datetime",
      "genres": [
        {
          "id": "uuid",
          "name": "string",
          "description": "string"
        }
      ],
      "production_companies": [
        {
          "id": "uuid",
          "name": "string",
          "logo_url": "string",
          "origin_country": "string"
        }
      ]
    }
  ]
}
```

#### 2. Get Movie Details
- **URL:** `GET /api/v1/movies/{id}/`
- **Permission:** AllowAny
- **Description:** Get detailed information about a specific movie

**Response Fields:**
```json
{
  "id": "uuid",
  "title": "string",
  "original_title": "string",
  "release_date": "date",
  "runtime": "integer",
  "budget": "integer",
  "revenue": "integer",
  "overview": "string",
  "tagline": "string",
  "poster_url": "string",
  "backdrop_url": "string",
  "trailer_url": "string",
  "imdb_id": "string",
  "tmdb_id": "integer",
  "status": "string",
  "adult": "boolean",
  "popularity_score": "float",
  "vote_average": "float",
  "vote_count": "integer",
  "is_featured": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime",
  "genres": [
    {
      "id": "uuid",
      "name": "string",
      "description": "string"
    }
  ],
  "production_companies": [
    {
      "id": "uuid",
      "name": "string",
      "logo_url": "string",
      "origin_country": "string"
    }
  ],
  "cast": [
    {
      "id": "uuid",
      "person": {
        "id": "uuid",
        "name": "string",
        "biography": "string",
        "birthday": "date",
        "deathday": "date",
        "place_of_birth": "string",
        "profile_image_url": "string",
        "imdb_id": "string",
        "tmdb_id": "integer"
      },
      "character_name": "string",
      "cast_order": "integer"
    }
  ],
  "crew": [
    {
      "id": "uuid",
      "person": {
        "id": "uuid",
        "name": "string",
        "biography": "string",
        "birthday": "date",
        "deathday": "date",
        "place_of_birth": "string",
        "profile_image_url": "string",
        "imdb_id": "string",
        "tmdb_id": "integer"
      },
      "job": "string",
      "department": "string"
    }
  ]
}
```

#### 3. Search Movies
- **URL:** `GET /api/v1/movies/search/`
- **Permission:** AllowAny
- **Description:** Search movies by title, overview, or other criteria
- **Query Parameters:**
  - `q` (string, required) - Search query
  - `page` (int, optional) - Page number

**Response:** Same as List Movies

#### 4. List Genres
- **URL:** `GET /api/v1/movies/genres/`
- **Permission:** AllowAny
- **Description:** List all movie genres

**Response Fields:**
```json
{
  "count": "integer",
  "next": "string (url)",
  "previous": "string (url)",
  "results": [
    {
      "id": "uuid",
      "name": "string",
      "description": "string",
      "created_at": "datetime",
      "movie_count": "integer"
    }
  ]
}
```

#### 5. Get Genre Details
- **URL:** `GET /api/v1/movies/genres/{id}/`
- **Permission:** AllowAny
- **Description:** Get genre details with associated movies

**Response Fields:**
```json
{
  "id": "uuid",
  "name": "string",
  "description": "string",
  "created_at": "datetime",
  "movies": [
    {
      "id": "uuid",
      "title": "string",
      "release_date": "date",
      "poster_url": "string",
      "vote_average": "float",
      "popularity_score": "float"
    }
  ]
}
```

#### 6. List Production Companies
- **URL:** `GET /api/v1/movies/production-companies/`
- **Permission:** AllowAny
- **Description:** List all production companies

**Response Fields:**
```json
{
  "count": "integer",
  "next": "string (url)",
  "previous": "string (url)",
  "results": [
    {
      "id": "uuid",
      "name": "string",
      "logo_url": "string",
      "origin_country": "string",
      "created_at": "datetime",
      "movie_count": "integer"
    }
  ]
}
```

#### 7. Get Production Company Details
- **URL:** `GET /api/v1/movies/production-companies/{id}/`
- **Permission:** AllowAny
- **Description:** Get production company details with associated movies

**Response Fields:**
```json
{
  "id": "uuid",
  "name": "string",
  "logo_url": "string",
  "origin_country": "string",
  "created_at": "datetime",
  "movies": [
    {
      "id": "uuid",
      "title": "string",
      "release_date": "date",
      "poster_url": "string",
      "vote_average": "float",
      "popularity_score": "float"
    }
  ]
}
```

#### 8. List People
- **URL:** `GET /api/v1/movies/people/`
- **Permission:** AllowAny
- **Description:** List all people (actors, directors, etc.)
- **Query Parameters:**
  - `search` (string, optional) - Search by name
  - `page` (int, optional) - Page number

**Response Fields:**
```json
{
  "count": "integer",
  "next": "string (url)",
  "previous": "string (url)",
  "results": [
    {
      "id": "uuid",
      "name": "string",
      "biography": "string",
      "birthday": "date",
      "deathday": "date",
      "place_of_birth": "string",
      "profile_image_url": "string",
      "imdb_id": "string",
      "tmdb_id": "integer",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ]
}
```

#### 9. Get Person Details
- **URL:** `GET /api/v1/movies/people/{id}/`
- **Permission:** AllowAny
- **Description:** Get person details with filmography

**Response Fields:**
```json
{
  "id": "uuid",
  "name": "string",
  "biography": "string",
  "birthday": "date",
  "deathday": "date",
  "place_of_birth": "string",
  "profile_image_url": "string",
  "imdb_id": "string",
  "tmdb_id": "integer",
  "created_at": "datetime",
  "updated_at": "datetime",
  "cast_roles": [
    {
      "movie": {
        "id": "uuid",
        "title": "string",
        "release_date": "date",
        "poster_url": "string"
      },
      "character_name": "string",
      "cast_order": "integer"
    }
  ],
  "crew_roles": [
    {
      "movie": {
        "id": "uuid",
        "title": "string",
        "release_date": "date",
        "poster_url": "string"
      },
      "job": "string",
      "department": "string"
    }
  ]
}
```

#### 10. Get Featured Movies
- **URL:** `GET /api/v1/movies/featured/`
- **Permission:** AllowAny
- **Description:** Get featured movies

**Response:** Same as List Movies (filtered for featured)

#### 11. Get Popular Movies
- **URL:** `GET /api/v1/movies/popular/`
- **Permission:** AllowAny
- **Description:** Get popular movies sorted by popularity score

**Response:** Same as List Movies (sorted by popularity)

#### 12. Get Top Rated Movies
- **URL:** `GET /api/v1/movies/top-rated/`
- **Permission:** AllowAny
- **Description:** Get top-rated movies sorted by vote average

**Response:** Same as List Movies (sorted by vote average)

#### 13. TMDB Search (Direct)
- **URL:** `GET /api/v1/movies/tmdb-search/`
- **Permission:** AllowAny
- **Description:** Search TMDB directly without syncing to database
- **Query Parameters:**
  - `q` (string, required) - Search query

**Response Fields:**
```json
{
  "query": "string",
  "tmdb_results": {
    "page": "integer",
    "results": [
      {
        "id": "integer",
        "title": "string",
        "original_title": "string",
        "overview": "string",
        "release_date": "date",
        "poster_path": "string",
        "backdrop_path": "string",
        "vote_average": "float",
        "vote_count": "integer",
        "popularity": "float",
        "adult": "boolean",
        "genre_ids": ["integer array"]
      }
    ],
    "total_pages": "integer",
    "total_results": "integer"
  }
}
```

### Admin Movie Endpoints (Admin Authentication Required)

#### 14. Create Movie
- **URL:** `POST /api/v1/movies/`
- **Permission:** IsAdminUser
- **Description:** Create a new movie

**Request Fields:**
```json
{
  "title": "string (required)",
  "original_title": "string (optional)",
  "release_date": "date (optional)",
  "runtime": "integer (optional)",
  "budget": "integer (optional)",
  "revenue": "integer (optional)",
  "overview": "string (optional)",
  "tagline": "string (optional)",
  "poster_url": "string (optional)",
  "backdrop_url": "string (optional)",
  "trailer_url": "string (optional)",
  "imdb_id": "string (optional)",
  "tmdb_id": "integer (optional)",
  "status": "string (optional)",
  "adult": "boolean (optional)",
  "popularity_score": "float (optional)",
  "vote_average": "float (optional)",
  "vote_count": "integer (optional)",
  "is_featured": "boolean (optional)",
  "genres": ["uuid array (optional)"],
  "production_companies": ["uuid array (optional)"]
}
```

**Response:** Same as Get Movie Details

#### 15. Update Movie
- **URL:** `PUT /api/v1/movies/{id}/`
- **Permission:** IsAdminUser
- **Description:** Update a movie (full update)

**Request Fields:** Same as Create Movie
**Response:** Same as Get Movie Details

#### 16. Partial Update Movie
- **URL:** `PATCH /api/v1/movies/{id}/`
- **Permission:** IsAdminUser
- **Description:** Partially update a movie

**Request Fields:** Same as Create Movie (all optional)
**Response:** Same as Get Movie Details

#### 17. Delete Movie
- **URL:** `DELETE /api/v1/movies/{id}/`
- **Permission:** IsAdminUser
- **Description:** Delete a movie

**Response:**
```json
{
  "message": "Movie deleted successfully"
}
```

#### 18. Sync Movie from TMDB
- **URL:** `POST /api/v1/movies/sync-from-tmdb/`
- **Permission:** IsAdminUser
- **Description:** Sync a specific movie from TMDB by ID

**Request Fields:**
```json
{
  "tmdb_id": "integer (required)"
}
```

**Response Fields:**
```json
{
  "message": "string",
  "movie": {
    "id": "uuid",
    "title": "string",
    "tmdb_id": "integer",
    "imdb_id": "string",
    "overview": "string",
    "release_date": "date",
    "poster_url": "string",
    "backdrop_url": "string",
    "vote_average": "float",
    "popularity_score": "float",
    "genres": ["array"],
    "production_companies": ["array"],
    "cast": ["array"],
    "crew": ["array"]
  }
}
```

#### 19. Sync Genres from TMDB
- **URL:** `POST /api/v1/movies/sync-genres-from-tmdb/`
- **Permission:** IsAdminUser
- **Description:** Sync all genres from TMDB

**Response Fields:**
```json
{
  "message": "string",
  "genres": [
    {
      "id": "uuid",
      "name": "string",
      "description": "string",
      "created_at": "datetime"
    }
  ]
}
```

#### 20. Create Genre
- **URL:** `POST /api/v1/movies/genres/`
- **Permission:** IsAdminUser
- **Description:** Create a new genre

**Request Fields:**
```json
{
  "name": "string (required)",
  "description": "string (optional)"
}
```

#### 21. Update Genre
- **URL:** `PUT /api/v1/movies/genres/{id}/`
- **Permission:** IsAdminUser
- **Description:** Update a genre

#### 22. Delete Genre
- **URL:** `DELETE /api/v1/movies/genres/{id}/`
- **Permission:** IsAdminUser
- **Description:** Delete a genre

#### 23. Create Production Company
- **URL:** `POST /api/v1/movies/production-companies/`
- **Permission:** IsAdminUser
- **Description:** Create a new production company

#### 24. Update Production Company
- **URL:** `PUT /api/v1/movies/production-companies/{id}/`
- **Permission:** IsAdminUser
- **Description:** Update a production company

#### 25. Delete Production Company
- **URL:** `DELETE /api/v1/movies/production-companies/{id}/`
- **Permission:** IsAdminUser
- **Description:** Delete a production company

#### 26. Create Person
- **URL:** `POST /api/v1/movies/people/`
- **Permission:** IsAdminUser
- **Description:** Create a new person

#### 27. Update Person
- **URL:** `PUT /api/v1/movies/people/{id}/`
- **Permission:** IsAdminUser
- **Description:** Update a person

#### 28. Delete Person
- **URL:** `DELETE /api/v1/movies/people/{id}/`
- **Permission:** IsAdminUser
- **Description:** Delete a person

## Additional Features

### Filtering and Search
- Full-text search across movie titles and overviews
- Filter by genre, year, status, rating
- Sort by popularity, rating, release date, title

### Performance Optimizations
- Database indexing on frequently queried fields
- Pagination for large result sets
- Optimized queries with select_related and prefetch_related

### Data Validation
- Unique constraints on IMDB ID and TMDB ID
- Date validation for release dates
- URL validation for image and trailer URLs
- Proper foreign key relationships

### Admin Features
- Django admin interface for all models
- Bulk operations for movies
- Import/export functionality
- Data validation and cleaning

## Security Features
- Public read access for all movie data
- Admin-only write access
- Proper permission checking
- Input validation and sanitization

## Database Configuration
- Uses UUID primary keys for all models
- Proper indexing for performance
- Foreign key relationships with proper cascading
- JSON fields for flexible data storage where needed

## Files Created/Modified

### New Files Created:
1. `apps/movies/__init__.py` - Movies app initialization
2. `apps/movies/apps.py` - App configuration
3. `apps/movies/models.py` - All movie-related models
4. `apps/movies/serializers.py` - All serializers for movies
5. `apps/movies/views.py` - All API views
6. `apps/movies/urls.py` - URL routing
7. `apps/movies/admin.py` - Admin configuration
8. `apps/movies/filters.py` - Django filters for search/filtering
9. `apps/movies/permissions.py` - Custom permissions
10. `apps/movies/services.py` - External API integrations (for future TMDB)
11. `apps/movies/tasks.py` - Celery tasks (for future async operations)

### Modified Files:
1. `movieexplained_backend/settings.py` - Add movies app to INSTALLED_APPS
2. `movieexplained_backend/urls.py` - Add movies API endpoints

## Next Steps for Stage 3
After Stage 2 completion, the next stage would include:
1. Content App (3.2.3) - Movie explanations and blog posts
2. AI Integration App (3.2.4) - Content generation
3. Recommendations App (3.2.5) - Movie recommendations
4. Analytics App (3.2.6) - User analytics and feedback
5. Admin Dashboard App (3.2.7) - Administrative interface
