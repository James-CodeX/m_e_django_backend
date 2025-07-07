# MovieExplained Backend

A Django REST API backend for the MovieExplained platform - an AI-powered movie blog website that provides comprehensive movie explanations, reviews, and recommendations.

## Project Status

### ✅ Stage 1: Authentication App (COMPLETED)
- ✅ User model with custom UUID primary keys
- ✅ UserPreferences model for user settings
- ✅ JWT authentication with token refresh and blacklisting
- ✅ Complete API endpoints for user registration, login, logout
- ✅ User profile management (view, update)
- ✅ User preferences management
- ✅ Password change functionality
- ✅ Custom permissions and validation
- ✅ API documentation with Swagger/ReDoc

### ✅ Stage 2: Movies App (COMPLETED)
- ✅ Movie model with comprehensive movie data
- ✅ Genre model for movie categorization
- ✅ ProductionCompany model for movie studios
- ✅ Person model for cast and crew
- ✅ MovieCast and MovieCrew models for relationships
- ✅ Complete API endpoints for all movie-related data
- ✅ Advanced filtering and search functionality
- ✅ Public read access, admin-only write access
- ✅ Django admin interface for all models
- ✅ Database migrations and optimization

### 🚧 Upcoming Stages
- 📋 Stage 3: Content App - Movie explanations and blog posts
- 📋 Stage 4: AI Integration App - Content generation
- 📋 Stage 5: Recommendations App - Movie recommendations
- 📋 Stage 6: Analytics App - User analytics and feedback
- 📋 Stage 7: Admin Dashboard App - Administrative interface

## Features

### Authentication & User Management
- Custom user model with email-based authentication
- JWT token authentication with refresh tokens
- User profile management with preferences
- Secure password validation and change
- Permission-based access control

### Movies & Media Data
- Comprehensive movie database with detailed metadata
- Genre and production company management
- Cast and crew information with roles
- Advanced search and filtering capabilities
- TMDB and IMDB ID support for external integration
- Featured movies and popularity-based sorting

### API Features
- RESTful API design with consistent endpoints
- Automatic API documentation (Swagger/ReDoc)
- Pagination for large datasets
- Advanced filtering with django-filters
- CORS support for frontend integration
- Comprehensive error handling and validation

## Technology Stack

- **Backend Framework**: Django 5.2.1
- **API Framework**: Django REST Framework
- **Authentication**: JWT (Simple JWT)
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Documentation**: drf-spectacular (OpenAPI 3.0)
- **Filtering**: django-filter
- **CORS**: django-cors-headers

## API Endpoints

### Authentication Endpoints
- `POST /api/v1/auth/register/` - User registration
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/logout/` - User logout
- `POST /api/v1/auth/refresh/` - Token refresh
- `GET /api/v1/auth/profile/` - Get user profile
- `PUT/PATCH /api/v1/auth/profile/` - Update user profile
- `GET/PUT/PATCH /api/v1/auth/preferences/` - User preferences
- `POST /api/v1/auth/change-password/` - Change password

### Movies Endpoints
- `GET /api/v1/movies/` - List movies (with filters)
- `GET /api/v1/movies/{id}/` - Movie details
- `GET /api/v1/movies/search/` - Search movies
- `GET /api/v1/movies/featured/` - Featured movies
- `GET /api/v1/movies/popular/` - Popular movies
- `GET /api/v1/movies/top-rated/` - Top-rated movies
- `POST/PUT/PATCH/DELETE /api/v1/movies/` - Admin-only movie management

### Genres Endpoints
- `GET /api/v1/genres/` - List genres
- `GET /api/v1/genres/{id}/` - Genre details with movies
- `POST/PUT/PATCH/DELETE /api/v1/genres/` - Admin-only genre management

### Production Companies Endpoints
- `GET /api/v1/production-companies/` - List production companies
- `GET /api/v1/production-companies/{id}/` - Company details with movies
- `POST/PUT/PATCH/DELETE /api/v1/production-companies/` - Admin-only company management

### People Endpoints
- `GET /api/v1/people/` - List people (actors, directors, etc.)
- `GET /api/v1/people/{id}/` - Person details with filmography
- `POST/PUT/PATCH/DELETE /api/v1/people/` - Admin-only people management

## Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd movieexplained-backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start development server**
   ```bash
   python manage.py runserver
   ```

## API Documentation

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## Database Models

### User Management
- `User` - Custom user model with email authentication
- `UserPreferences` - User settings and preferences

### Movies & Media
- `Movie` - Main movie model with comprehensive metadata
- `Genre` - Movie genres
- `ProductionCompany` - Movie production companies
- `Person` - Actors, directors, and crew members
- `MovieGenre` - Movie-genre relationships
- `MovieProductionCompany` - Movie-company relationships
- `MovieCast` - Movie cast relationships with character names
- `MovieCrew` - Movie crew relationships with job titles

## Security Features

- JWT-based authentication with token blacklisting
- Custom permissions for read-only public access and admin-only writes
- Input validation and sanitization
- CORS configuration for frontend integration
- Password validation with Django's built-in validators

## Performance Features

- Database indexing on frequently queried fields
- Optimized queries with select_related and prefetch_related
- Pagination for large datasets
- Efficient API serialization

## Development Features

- Comprehensive Django admin interface
- API documentation with interactive testing
- Custom management commands (extensible)
- Detailed logging and error handling
- Code organization with Django apps

## Contributing

1. Follow Django best practices
2. Write tests for new features
3. Update API documentation
4. Follow the existing code style
5. Create migrations for model changes

## License

[License information to be added]

---

**Project Status**: Stage 1 and 2 Complete ✅
**Next Stage**: Content App (Movie explanations and blog posts)
**Last Updated**: July 7, 2025
