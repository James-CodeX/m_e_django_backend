# Search Feature Implementation

## Overview

The search feature in the MovieExplained backend allows users to query for movies. If a movie exists in the local database, it's returned immediately. If not found locally, the system leverages the TMDB API to fetch movie data, which is then stored in the local database and returned to the user. This ensures that users receive results even for newly released or less common movies that are not yet in our database.

---

## How the Search Works

1. **User Initiates Search**:
    - The user makes a GET request to the `/api/v1/movies/search/` endpoint with the desired movie title as the query parameter.

2. **Local Database Search**:
    - The system first searches the local movies table using the provided query.
    - Fields searched include:
      - `title`
      - `original_title`
      - `overview`

3. **If Movie Found Locally**:
    - If the movie is found in the local database, it is returned immediately as a part of the response.
    - The response includes all movie details along with genres, production companies, cast, and crew.

4. **If Movie Not Found Locally**:
    - The system will initiate a search on TMDB using the TMDB API.
    - It searches for the movie title using TMDB’s search capabilities.

5. **TMDB Search Results**:
    - If TMDB finds relevant results, they are fetched and relevant data is imported.
    - The following actions occur:
      - **Movie Record Creation**: A new entry is created in the local movies table.
      - **Associated Records Creation**: Data related to genres, production companies, cast, and crew is also fetched and stored.

6. **Response and Data Synchronization**:
    - Once fetched and stored, TMDB results (now part of the local database) are returned to the user.
    - Search statistics are included, indicating results counts from local and TMDB searches, as well as newly synced movies.

---

## Involved Endpoints

### 1. **Movie Search Endpoint**
- **URL**: `/api/v1/movies/search/`
- **Method**: GET
- **Description**: Search movies, leveraging local and TMDB origins.
- **Parameters**:
  - `q`: (required) Movie title / query string.
  - `include_tmdb`: (optional, default: true) Determines if TMDB should be queried when not found locally.
  - `sync_missing`: (optional, default: true) If true, missing movies found on TMDB are synced into the local database.

### 2. **TMDB Direct Search Endpoint**
- **URL**: `/api/v1/movies/tmdb-search/`
- **Method**: GET
- **Description**: Search directly on TMDB without syncing data into local database.
- **Parameters**:
  - `q`: (required) Movie title / query string.

---

## Database Tables Involved

### Primary Tables
1. **`movies`** - Main movie table storing comprehensive movie data
2. **`genres`** - Movie genres (Action, Drama, etc.)
3. **`production_companies`** - Movie studios and production companies
4. **`people`** - Actors, directors, and crew members

### Relationship Tables
1. **`movie_genres`** - Links movies to their genres
2. **`movie_production_companies`** - Links movies to production companies
3. **`movie_cast`** - Links movies to cast members with character names
4. **`movie_crew`** - Links movies to crew members with job titles

### Fields Populated from TMDB

#### Movie Fields
- `tmdb_id` - TMDB identifier for the movie
- `title` - Movie title
- `original_title` - Original language title
- `overview` - Movie plot summary
- `tagline` - Movie tagline
- `release_date` - Release date
- `runtime` - Duration in minutes
- `budget` - Production budget
- `revenue` - Box office revenue
- `status` - Release status (released, upcoming, in_production)
- `adult` - Adult content flag
- `popularity_score` - TMDB popularity score
- `vote_average` - TMDB user rating
- `vote_count` - Number of votes
- `poster_url` - Movie poster image URL
- `backdrop_url` - Backdrop image URL
- `imdb_id` - IMDB identifier

#### Associated Data
- **Genres**: Name and description
- **Production Companies**: Name, logo, origin country
- **Cast Members**: Name, character, profile image, biography
- **Crew Members**: Name, job title, department, profile image

---

## Important Classes & Methods

### 1. `MovieViewSet` (apps/movies/views.py)
- **Location**: `apps/movies/views.py`
- **Method**: `search(self, request)`
- **Functionality**:
  - Handles incoming search requests
  - Coordinates local database search and TMDB integration
  - Returns comprehensive search results with statistics

### 2. `MovieSearchService` (apps/movies/services.py)
- **Location**: `apps/movies/services.py`
- **Method**: `comprehensive_search(self, query, include_tmdb=True)`
- **Functionality**:
  - Performs local database search first
  - Triggers TMDB search if no local results
  - Coordinates movie synchronization
  - Returns combined results

### 3. `TMDBService` (apps/movies/services.py)
- **Location**: `apps/movies/services.py`
- **Key Methods**:
  - `search_movies(query)` - Search TMDB for movies
  - `fetch_movie_data(tmdb_id)` - Get detailed movie data
  - `fetch_person_data(tmdb_id)` - Get cast/crew details
  - `fetch_genre_list()` - Get all available genres
- **Functionality**:
  - Direct TMDB API communication
  - Handles API authentication and rate limiting
  - Formats TMDB responses for local consumption

### 4. `MovieDataService` (apps/movies/services.py)
- **Location**: `apps/movies/services.py`
- **Key Methods**:
  - `sync_movie_from_tmdb(tmdb_id)` - Create movie record from TMDB data
  - `search_and_sync_movies(query)` - Search and sync multiple movies
  - `_get_or_create_genre(genre_data)` - Handle genre creation
  - `_get_or_create_person(person_data)` - Handle cast/crew creation
- **Functionality**:
  - Manages database transactions for movie synchronization
  - Handles relationships between movies and associated data
  - Prevents duplicate records

---

## Search Flow Diagram

```
User Request: GET /api/v1/movies/search/?q=Inception
        ↓
[MovieViewSet.search()]
        ↓
[MovieSearchService.comprehensive_search()]
        ↓
1. Search Local Database
   Query: Movie.objects.filter(
     Q(title__icontains=query) |
     Q(original_title__icontains=query) |
     Q(overview__icontains=query)
   )
        ↓
2. Local Results Found?
   ├─ YES → Return local results
   └─ NO → Continue to TMDB
        ↓
3. [TMDBService.search_movies()]
   → Call TMDB API: /search/movie
        ↓
4. TMDB Results Found?
   ├─ NO → Return empty results
   └─ YES → Continue to sync
        ↓
5. [MovieDataService.search_and_sync_movies()]
   For each TMDB result (max 5):
   ├─ [TMDBService.fetch_movie_data()]
   │  → Get detailed movie data + credits
   ├─ [MovieDataService.sync_movie_from_tmdb()]
   │  → Create Movie record
   │  → Create/link Genres
   │  → Create/link Production Companies
   │  → Create/link Cast (top 20)
   │  → Create/link Crew (key roles)
   └─ Add to synced_movies list
        ↓
6. Return Response:
   {
     "query": "Inception",
     "results": [synced_movies],
     "search_stats": {
       "local_count": 0,
       "tmdb_count": 10,
       "synced_count": 1,
       "total_count": 1
     }
   }
```

---

## Example API Requests and Responses

### Request 1: First Time Search (Movie Not in Database)

**Request:**
```bash
GET /api/v1/movies/search/?q=Inception&include_tmdb=true&sync_missing=true
```

**Response:**
```json
{
  "query": "Inception",
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Inception",
      "original_title": "Inception",
      "release_date": "2010-07-16",
      "release_year": 2010,
      "runtime": 148,
      "budget": 160000000,
      "revenue": 836836967,
      "overview": "Cobb, a skilled thief who commits corporate espionage...",
      "tagline": "Your mind is the scene of the crime.",
      "poster_url": "https://image.tmdb.org/t/p/w500/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
      "backdrop_url": "https://image.tmdb.org/t/p/w1280/aej3LvH7gbKO1AuwflY5epHjeI8.jpg",
      "trailer_url": "",
      "imdb_id": "tt1375666",
      "tmdb_id": 27205,
      "status": "released",
      "adult": false,
      "popularity_score": 83.414,
      "vote_average": 8.4,
      "vote_count": 35000,
      "is_featured": false,
      "created_at": "2025-07-07T09:00:00Z",
      "updated_at": "2025-07-07T09:00:00Z",
      "genres": [
        {
          "id": "genre-uuid-1",
          "name": "Action",
          "description": "Genre: Action"
        },
        {
          "id": "genre-uuid-2",
          "name": "Science Fiction",
          "description": "Genre: Science Fiction"
        },
        {
          "id": "genre-uuid-3",
          "name": "Thriller",
          "description": "Genre: Thriller"
        }
      ],
      "production_companies": [
        {
          "id": "company-uuid-1",
          "name": "Warner Bros. Pictures",
          "logo_url": "https://image.tmdb.org/t/p/w500/logo.png",
          "origin_country": "US"
        },
        {
          "id": "company-uuid-2",
          "name": "Legendary Entertainment",
          "logo_url": "https://image.tmdb.org/t/p/w500/logo2.png",
          "origin_country": "US"
        }
      ]
    }
  ],
  "search_stats": {
    "local_count": 0,
    "tmdb_count": 15,
    "synced_count": 1,
    "total_count": 1
  }
}
```

### Request 2: Second Search (Movie Now in Database)

**Request:**
```bash
GET /api/v1/movies/search/?q=Inception&include_tmdb=true&sync_missing=true
```

**Response:**
```json
{
  "query": "Inception",
  "results": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Inception",
      // ... same movie data as above
    }
  ],
  "search_stats": {
    "local_count": 1,
    "tmdb_count": 0,
    "synced_count": 0,
    "total_count": 1
  }
}
```

### Request 3: Direct TMDB Search (No Database Sync)

**Request:**
```bash
GET /api/v1/movies/tmdb-search/?q=Inception
```

**Response:**
```json
{
  "query": "Inception",
  "tmdb_results": {
    "page": 1,
    "results": [
      {
        "id": 27205,
        "title": "Inception",
        "original_title": "Inception",
        "overview": "Cobb, a skilled thief who commits corporate espionage...",
        "release_date": "2010-07-16",
        "poster_path": "/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
        "backdrop_path": "/aej3LvH7gbKO1AuwflY5epHjeI8.jpg",
        "vote_average": 8.4,
        "vote_count": 35000,
        "popularity": 83.414,
        "adult": false,
        "genre_ids": [28, 878, 53]
      }
    ],
    "total_pages": 1,
    "total_results": 1
  }
}
```

---

## Error Handling

### Common Error Scenarios

1. **Missing Query Parameter**
   ```json
   {
     "detail": "Search query parameter 'q' is required."
   }
   ```

2. **TMDB API Error**
   ```json
   {
     "detail": "Search failed: TMDB API request failed"
   }
   ```

3. **Database Sync Error**
   ```json
   {
     "detail": "Sync failed: Database transaction error"
   }
   ```

---

## Performance Considerations

### Optimization Strategies
1. **Database Indexing**: Indexes on `title`, `original_title`, and `tmdb_id` fields
2. **Query Optimization**: Uses `select_related()` and `prefetch_related()` for efficient data loading
3. **Rate Limiting**: TMDB API calls are managed to respect rate limits
4. **Caching**: Future enhancement to cache TMDB responses
5. **Batch Processing**: Multiple movies synced in single database transaction

### Database Impact
- **New Movie**: Creates 1 movie record + associated genres, companies, cast, crew
- **Typical Sync**: 1 movie + 3-5 genres + 2-3 companies + 20 cast + 8-10 crew = ~35-40 database records
- **Transaction Safety**: All operations wrapped in database transactions

---

## Configuration

### Environment Variables
```bash
TMDB_API_KEY=your_api_key_here
TMDB_ACCESS_TOKEN=your_access_token_here
```

### Django Settings
```python
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p'
TMDB_IMAGE_SIZES = {
    'poster': 'w500',
    'backdrop': 'w1280', 
    'profile': 'w185'
}
```

---

## Technology and Libraries Used

- **Django**: Core framework for backend operations
- **Django REST Framework**: Enables creating RESTful APIs
- **TMDB API**: External movie database API used for fetching comprehensive movie data
- **Requests**: HTTP library for TMDB API communication
- **Logging**: Implemented across processes to trace and debug operations
- **UUID**: For unique record identifiers
- **Database Transactions**: Ensures data consistency during sync operations

---

## Security & Permissions

- Access to certain endpoints, such as syncing or admin tasks, is restricted to authenticated users with proper permissions.
- API keys and sensitive data are secured using environment variables.

---

This search feature implementation provides a robust mechanism to ensure users always receive up-to-date movie information, whether from our local database or via the broad reach of the TMDB API.
