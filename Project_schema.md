MovieExplained - backend

1. Project Overview
1.1 Project Description
MovieExplained is an AI-powered movie blog website that provides comprehensive movie explanations, reviews, and recommendations. The platform combines automated content generation with manual curation through an admin dashboard.

1.2 Key Features
Movie Explanations: Detailed breakdowns of movies including plot, themes, and analysis
Genre Classification: Automatic categorization and genre-based recommendations
Blog Section: Curated articles about best movies of specific periods
AI Integration: Automated content generation and recommendations
Admin Dashboard: Complete content management and analytics system
User Feedback: Rating and comment system with sentiment analysis

2. Database Schema Design
2.1 Core Models
2.1.1 User Management
-- Users table
users:
  - id (UUID, Primary Key)
  - email (Unique, Not Null)
  - username (Unique, Not Null)
  - password_hash (Not Null)
  - first_name (Varchar 50)
  - last_name (Varchar 50)
  - is_admin (Boolean, Default: False)
  - is_active (Boolean, Default: True)
  - date_joined (Timestamp)
  - last_login (Timestamp)
  - profile_image (URL)
  - bio (Text)

-- User preferences
user_preferences:
  - id (UUID, Primary Key)
  - user_id (Foreign Key -> users.id)
  - favorite_genres (JSON Array)
  - preferred_languages (JSON Array)
  - email_notifications (Boolean)
  - created_at (Timestamp)
  - updated_at (Timestamp)

2.1.2 Movie Data
-- Movies table
movies:
  - id (UUID, Primary Key)
  - title (Varchar 200, Not Null)
  - original_title (Varchar 200)
  - release_date (Date)
  - runtime (Integer) -- minutes
  - budget (BigInteger)
  - revenue (BigInteger)
  - overview (Text)
  - tagline (Varchar 500)
  - poster_url (URL)
  - backdrop_url (URL)
  - trailer_url (URL)
  - imdb_id (Varchar 20, Unique)
  - tmdb_id (Integer, Unique)
  - status (Enum: released, upcoming, in_production)
  - adult (Boolean, Default: False)
  - popularity_score (Float)
  - vote_average (Float)
  - vote_count (Integer)
  - created_at (Timestamp)
  - updated_at (Timestamp)
  - is_featured (Boolean, Default: False)

-- Genres table
genres:
  - id (UUID, Primary Key)
  - name (Varchar 50, Unique)
  - description (Text)
  - created_at (Timestamp)

-- Movie-Genre relationship
movie_genres:
  - id (UUID, Primary Key)
  - movie_id (Foreign Key -> movies.id)
  - genre_id (Foreign Key -> genres.id)
  - created_at (Timestamp)

-- Production companies
production_companies:
  - id (UUID, Primary Key)
  - name (Varchar 100, Unique)
  - logo_url (URL)
  - origin_country (Varchar 2)
  - created_at (Timestamp)

-- Movie-Production Company relationship
movie_production_companies:
  - id (UUID, Primary Key)
  - movie_id (Foreign Key -> movies.id)
  - company_id (Foreign Key -> production_companies.id)

-- Cast and Crew
people:
  - id (UUID, Primary Key)
  - name (Varchar 100, Not Null)
  - biography (Text)
  - birthday (Date)
  - deathday (Date)
  - place_of_birth (Varchar 200)
  - profile_image_url (URL)
  - imdb_id (Varchar 20, Unique)
  - tmdb_id (Integer, Unique)
  - created_at (Timestamp)
  - updated_at (Timestamp)

-- Movie Cast
movie_cast:
  - id (UUID, Primary Key)
  - movie_id (Foreign Key -> movies.id)
  - person_id (Foreign Key -> people.id)
  - character_name (Varchar 200)
  - cast_order (Integer)
  - created_at (Timestamp)

-- Movie Crew
movie_crew:
  - id (UUID, Primary Key)
  - movie_id (Foreign Key -> movies.id)
  - person_id (Foreign Key -> people.id)
  - job (Varchar 100)
  - department (Varchar 50)
  - created_at (Timestamp)

2.1.3 Content Management
-- Movie explanations/reviews
movie_explanations:
  - id (UUID, Primary Key)
  - movie_id (Foreign Key -> movies.id)
  - title (Varchar 200, Not Null)
  - content (Text, Not Null)
  - summary (Text)
  - explanation_type (Enum: plot_summary, detailed_analysis, ending_explained, themes)
  - ai_generated (Boolean, Default: False)
  - author_id (Foreign Key -> users.id, Nullable)
  - status (Enum: draft, published, archived)
  - seo_title (Varchar 200)
  - seo_description (Varchar 300)
  - slug (Varchar 200, Unique)
  - featured_image_url (URL)
  - reading_time (Integer) -- minutes
  - view_count (Integer, Default: 0)
  - created_at (Timestamp)
  - updated_at (Timestamp)
  - published_at (Timestamp)

-- Blog posts
blog_posts:
  - id (UUID, Primary Key)
  - title (Varchar 200, Not Null)
  - content (Text, Not Null)
  - excerpt (Text)
  - category (Enum: best_of_year, genre_analysis, director_spotlight, industry_news)
  - author_id (Foreign Key -> users.id)
  - status (Enum: draft, published, archived)
  - seo_title (Varchar 200)
  - seo_description (Varchar 300)
  - slug (Varchar 200, Unique)
  - featured_image_url (URL)
  - reading_time (Integer)
  - view_count (Integer, Default: 0)
  - is_featured (Boolean, Default: False)
  - created_at (Timestamp)
  - updated_at (Timestamp)
  - published_at (Timestamp)

-- Blog post - Movie relationships
blog_post_movies:
  - id (UUID, Primary Key)
  - blog_post_id (Foreign Key -> blog_posts.id)
  - movie_id (Foreign Key -> movies.id)
  - created_at (Timestamp)

-- Tags
tags:
  - id (UUID, Primary Key)
  - name (Varchar 50, Unique)
  - slug (Varchar 50, Unique)
  - description (Text)
  - created_at (Timestamp)

-- Content tagging
content_tags:
  - id (UUID, Primary Key)
  - content_type (Enum: movie_explanation, blog_post)
  - content_id (UUID)
  - tag_id (Foreign Key -> tags.id)
  - created_at (Timestamp)

2.1.4 User Engagement
-- Comments
comments:
  - id (UUID, Primary Key)
  - content_type (Enum: movie_explanation, blog_post)
  - content_id (UUID)
  - user_id (Foreign Key -> users.id)
  - parent_id (Foreign Key -> comments.id, Nullable)
  - content (Text, Not Null)
  - is_approved (Boolean, Default: False)
  - is_flagged (Boolean, Default: False)
  - created_at (Timestamp)
  - updated_at (Timestamp)

-- Ratings
ratings:
  - id (UUID, Primary Key)
  - content_type (Enum: movie, movie_explanation, blog_post)
  - content_id (UUID)
  - user_id (Foreign Key -> users.id)
  - rating (Integer, Check: 1-5)
  - created_at (Timestamp)
  - updated_at (Timestamp)

-- User bookmarks/favorites
bookmarks:
  - id (UUID, Primary Key)
  - user_id (Foreign Key -> users.id)
  - content_type (Enum: movie, movie_explanation, blog_post)
  - content_id (UUID)
  - created_at (Timestamp)

-- User reading history
reading_history:
  - id (UUID, Primary Key)
  - user_id (Foreign Key -> users.id)
  - content_type (Enum: movie_explanation, blog_post)
  - content_id (UUID)
  - read_at (Timestamp)
  - reading_progress (Float) -- percentage

2.1.5 AI and Recommendations
-- AI generation logs
ai_generation_logs:
  - id (UUID, Primary Key)
  - content_type (Enum: movie_explanation, blog_post, recommendation)
  - content_id (UUID)
  - ai_model (Varchar 50)
  - prompt_used (Text)
  - tokens_used (Integer)
  - generation_time (Float) -- seconds
  - status (Enum: success, failed, partial)
  - error_message (Text)
  - created_at (Timestamp)

-- Movie recommendations
movie_recommendations:
  - id (UUID, Primary Key)
  - movie_id (Foreign Key -> movies.id)
  - recommended_movie_id (Foreign Key -> movies.id)
  - recommendation_type (Enum: similar_plot, same_genre, same_director, ai_generated)
  - score (Float)
  - reason (Text)
  - created_at (Timestamp)

-- User recommendations
user_recommendations:
  - id (UUID, Primary Key)
  - user_id (Foreign Key -> users.id)
  - movie_id (Foreign Key -> movies.id)
  - recommendation_score (Float)
  - reason (Text)
  - is_clicked (Boolean, Default: False)
  - created_at (Timestamp)

2.1.6 Analytics and Feedback
-- Analytics events
analytics_events:
  - id (UUID, Primary Key)
  - event_type (Enum: page_view, content_view, search, click, share)
  - user_id (Foreign Key -> users.id, Nullable)
  - session_id (Varchar 100)
  - content_type (Enum: movie, movie_explanation, blog_post)
  - content_id (UUID, Nullable)
  - metadata (JSON)
  - ip_address (Inet)
  - user_agent (Text)
  - referrer (URL)
  - created_at (Timestamp)

-- Feedback
feedback:
  - id (UUID, Primary Key)
  - user_id (Foreign Key -> users.id, Nullable)
  - content_type (Enum: movie_explanation, blog_post, site_general)
  - content_id (UUID, Nullable)
  - feedback_type (Enum: bug_report, feature_request, content_feedback, general)
  - title (Varchar 200)
  - description (Text, Not Null)
  - status (Enum: open, in_progress, resolved, closed)
  - priority (Enum: low, medium, high, urgent)
  - admin_response (Text)
  - created_at (Timestamp)
  - updated_at (Timestamp)
  - resolved_at (Timestamp)

-- Search analytics
search_analytics:
  - id (UUID, Primary Key)
  - user_id (Foreign Key -> users.id, Nullable)
  - query (Varchar 200)
  - results_count (Integer)
  - clicked_result_id (UUID, Nullable)
  - clicked_result_type (Enum: movie, movie_explanation, blog_post)
  - created_at (Timestamp)

3. Backend Architecture (Django)
3.1 Project Structure
movieexplained_backend/
├── manage.py
├── requirements.txt
├── .env.example
├── movieexplained/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── testing.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── __init__.py
│   ├── authentication/
│   ├── movies/
│   ├── content/
│   ├── analytics/
│   ├── ai_integration/
│   ├── recommendations/
│   └── admin_dashboard/
├── utils/
│   ├── __init__.py
│   ├── permissions.py
│   ├── pagination.py
│   ├── validators.py
│   └── helpers.py
├── tests/
└── media/

3.2 App Structure Details
3.2.1 Authentication App
apps/authentication/
├── __init__.py
├── models.py          # User, UserProfile, UserPreferences
├── serializers.py     # User serialization
├── views.py          # Login, Register, Profile management
├── permissions.py    # Custom permissions
├── urls.py
├── managers.py       # Custom user manager
└── admin.py

3.2.2 Movies App
apps/movies/
├── __init__.py
├── models.py          # Movie, Genre, Person, Cast, Crew
├── serializers.py     # Movie data serialization
├── views.py          # Movie CRUD, Search, Filters
├── urls.py
├── admin.py
├── tasks.py          # Celery tasks for movie data sync
├── services.py       # External API integrations (TMDB)
└── filters.py        # Django filters for movie search

3.2.3 Content App
apps/content/
├── __init__.py
├── models.py          # MovieExplanation, BlogPost, Comment, Rating
├── serializers.py     # Content serialization
├── views.py          # Content CRUD, Publishing workflow
├── urls.py
├── admin.py
├── tasks.py          # Content processing tasks
├── services.py       # Content generation services
└── editors.py        # Rich text editor integration

3.2.4 AI Integration App
apps/ai_integration/
├── __init__.py
├── models.py          # AIGenerationLog
├── services.py       # OpenAI integration, content generation
├── tasks.py          # Async AI processing
├── prompts.py        # AI prompt templates
└── utils.py          # AI helper functions

3.2.5 Recommendations App
apps/recommendations/
├── __init__.py
├── models.py          # MovieRecommendation, UserRecommendation
├── services.py       # Recommendation algorithms
├── tasks.py          # Recommendation generation tasks
├── ml_models.py      # Custom ML models
└── utils.py          # Recommendation utilities

3.2.6 Analytics App
apps/analytics/
├── __init__.py
├── models.py          # AnalyticsEvent, SearchAnalytics, Feedback
├── serializers.py     # Analytics data serialization
├── views.py          # Analytics endpoints
├── urls.py
├── services.py       # Analytics processing
└── reports.py        # Report generation

3.2.7 Admin Dashboard App
apps/admin_dashboard/
├── __init__.py
├── views.py          # Dashboard views and stats
├── serializers.py    # Dashboard data serialization
├── urls.py
├── permissions.py    # Admin permissions
├── services.py       # Dashboard services
└── reports.py        # Admin reports

3.3 Key Django Settings
3.3.1 Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    'celery',
    'django_redis',
    'storages',
    
    # Local apps
    'apps.authentication',
    'apps.movies',
    'apps.content',
    'apps.ai_integration',
    'apps.recommendations',
    'apps.analytics',
    'apps.admin_dashboard',
]

3.3.2 API Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',  # Key setting for public read access
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Custom permission classes for specific endpoints
CUSTOM_PERMISSIONS = {
    'READ_ONLY_ENDPOINTS': [
        'movies.*',
        'content.explanations.*',
        'content.blog-posts.*',
        'content.comments.list',
        'content.ratings.list',
    ],
    'AUTH_REQUIRED_ENDPOINTS': [
        'content.comments.create',
        'content.comments.update',
        'content.comments.delete',
        'content.ratings.create',
        'content.ratings.update',
        'user.*',
        'bookmarks.*',
    ]
}

3.4 Key API Endpoints
3.4.1 Public API Endpoints (No Authentication Required)
GET /api/v1/movies/                     # List movies with filters
GET /api/v1/movies/{id}/                # Movie details
GET /api/v1/movies/{id}/explanations/   # Movie explanations
GET /api/v1/movies/{id}/recommendations/ # Movie recommendations
GET /api/v1/movies/genres/              # List genres
GET /api/v1/movies/search/              # Search movies

GET /api/v1/content/explanations/       # List explanations
GET /api/v1/content/explanations/{id}/  # Explanation details
GET /api/v1/content/blog-posts/         # List blog posts
GET /api/v1/content/blog-posts/{id}/    # Blog post details

GET /api/v1/content/featured/           # Featured content
GET /api/v1/content/trending/           # Trending content

GET /api/v1/content/comments/{content_id}/ # View comments (read-only)
GET /api/v1/content/ratings/{content_id}/  # View ratings (read-only)

3.4.2 Authenticated User Endpoints (Login Required)
POST /api/v1/auth/register/             # User registration
POST /api/v1/auth/login/                # User login
POST /api/v1/auth/refresh/              # Token refresh
POST /api/v1/auth/logout/               # User logout

GET /api/v1/user/profile/               # User profile
PUT /api/v1/user/profile/               # Update profile
GET /api/v1/user/bookmarks/             # User bookmarks
POST /api/v1/user/bookmarks/            # Add bookmark
DELETE /api/v1/user/bookmarks/{id}/     # Remove bookmark

GET /api/v1/user/recommendations/       # Personalized recommendations
GET /api/v1/user/reading-history/       # Reading history

# Interactive Features (Authentication Required)
POST /api/v1/content/comments/          # Add comment
PUT /api/v1/content/comments/{id}/      # Update comment
DELETE /api/v1/content/comments/{id}/   # Delete comment

POST /api/v1/content/ratings/           # Add rating
PUT /api/v1/content/ratings/{id}/       # Update rating

POST /api/v1/feedback/                  # Submit feedback

3.4.3 Admin Endpoints
GET /api/v1/admin/dashboard/stats/      # Dashboard statistics
GET /api/v1/admin/analytics/            # Analytics data
GET /api/v1/admin/feedback/             # Feedback management

POST /api/v1/admin/movies/              # Add movie
PUT /api/v1/admin/movies/{id}/          # Update movie
DELETE /api/v1/admin/movies/{id}/       # Delete movie

POST /api/v1/admin/content/explanations/ # Create explanation
PUT /api/v1/admin/content/explanations/{id}/ # Update explanation
DELETE /api/v1/admin/content/explanations/{id}/ # Delete explanation

POST /api/v1/admin/content/blog-posts/  # Create blog post
PUT /api/v1/admin/content/blog-posts/{id}/ # Update blog post
DELETE /api/v1/admin/content/blog-posts/{id}/ # Delete blog post

POST /api/v1/admin/ai/generate-content/ # Generate AI content
GET /api/v1/admin/ai/generation-logs/   # AI generation logs

GET /api/v1/admin/users/                # User management
PUT /api/v1/admin/users/{id}/           # Update user
DELETE /api/v1/admin/users/{id}/        # Delete user


