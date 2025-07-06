# Stage 1: Authentication App Implementation

## Overview
This document details the implementation of Stage 1 (3.2.1 Authentication App) of the MovieExplained backend project.

## Models Implemented

### 1. User Model
**Table:** `users`
**Fields:**
- `id` (UUID, Primary Key)
- `email` (EmailField, Unique, Required)
- `username` (CharField, Unique, Required, max_length=150)
- `password` (CharField, handled by AbstractUser)
- `first_name` (CharField, max_length=50, Optional)
- `last_name` (CharField, max_length=50, Optional)
- `is_admin` (BooleanField, default=False)
- `is_active` (BooleanField, default=True)
- `date_joined` (DateTimeField, auto_now_add=True)
- `last_login` (DateTimeField, Optional)
- `profile_image` (URLField, Optional)
- `bio` (TextField, Optional)

**Additional Properties:**
- `full_name` (computed property)
- Custom Manager: `UserManager`
- Authentication Field: `email` (instead of username)

### 2. UserPreferences Model
**Table:** `user_preferences`
**Fields:**
- `id` (UUID, Primary Key)
- `user` (OneToOneField to User)
- `favorite_genres` (JSONField, default=[])
- `preferred_languages` (JSONField, default=[])
- `email_notifications` (BooleanField, default=True)
- `created_at` (DateTimeField, auto_now_add=True)
- `updated_at` (DateTimeField, auto_now=True)

## API Endpoints

### Authentication Endpoints

#### 1. User Registration
- **URL:** `POST /api/v1/auth/register/`
- **Permission:** AllowAny
- **Description:** Register a new user account

**Request Fields:**
```json
{
  "email": "string (required)",
  "username": "string (required)",
  "password": "string (required)",
  "password_confirm": "string (required)",
  "first_name": "string (optional)",
  "last_name": "string (optional)",
  "bio": "string (optional)",
  "profile_image": "string (url, optional)"
}
```

**Response Fields:**
```json
{
  "user": {
    "id": "uuid",
    "email": "string",
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "full_name": "string",
    "bio": "string",
    "profile_image": "string",
    "is_admin": "boolean",
    "date_joined": "datetime",
    "last_login": "datetime",
    "preferences": {
      "id": "uuid",
      "favorite_genres": "array",
      "preferred_languages": "array",
      "email_notifications": "boolean",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  },
  "refresh": "string (JWT)",
  "access": "string (JWT)",
  "message": "string"
}
```

#### 2. User Login
- **URL:** `POST /api/v1/auth/login/`
- **Permission:** AllowAny
- **Description:** Authenticate user and return JWT tokens

**Request Fields:**
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

**Response Fields:**
```json
{
  "user": {
    "id": "uuid",
    "email": "string",
    "username": "string",
    "first_name": "string",
    "last_name": "string",
    "full_name": "string",
    "bio": "string",
    "profile_image": "string",
    "is_admin": "boolean",
    "date_joined": "datetime",
    "last_login": "datetime",
    "preferences": "object"
  },
  "refresh": "string (JWT)",
  "access": "string (JWT)",
  "message": "string"
}
```

#### 3. User Logout
- **URL:** `POST /api/v1/auth/logout/`
- **Permission:** IsAuthenticated
- **Description:** Logout user by blacklisting refresh token

**Request Fields:**
```json
{
  "refresh": "string (JWT token, optional)"
}
```

**Response Fields:**
```json
{
  "message": "string"
}
```

#### 4. Token Refresh
- **URL:** `POST /api/v1/auth/refresh/`
- **Permission:** AllowAny
- **Description:** Refresh access token using refresh token

**Request Fields:**
```json
{
  "refresh": "string (JWT refresh token)"
}
```

**Response Fields:**
```json
{
  "access": "string (new JWT access token)"
}
```

### User Profile Endpoints

#### 5. Get User Profile
- **URL:** `GET /api/v1/auth/profile/`
- **Permission:** IsAuthenticated
- **Description:** Get current user profile

**Response Fields:**
```json
{
  "id": "uuid",
  "email": "string",
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "full_name": "string",
  "bio": "string",
  "profile_image": "string",
  "is_admin": "boolean",
  "date_joined": "datetime",
  "last_login": "datetime",
  "preferences": {
    "id": "uuid",
    "favorite_genres": "array",
    "preferred_languages": "array",
    "email_notifications": "boolean",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
}
```

#### 6. Update User Profile (Full Update)
- **URL:** `PUT /api/v1/auth/profile/`
- **Permission:** IsAuthenticated
- **Description:** Update current user profile (full update)

**Request Fields:**
```json
{
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "profile_image": "string (url)"
}
```

**Response:** Same as Get User Profile

#### 7. Update User Profile (Partial Update)
- **URL:** `PATCH /api/v1/auth/profile/`
- **Permission:** IsAuthenticated
- **Description:** Partially update current user profile

**Request Fields:** (all optional)
```json
{
  "first_name": "string (optional)",
  "last_name": "string (optional)",
  "bio": "string (optional)",
  "profile_image": "string (url, optional)"
}
```

**Response:** Same as Get User Profile

#### 8. Get User Preferences
- **URL:** `GET /api/v1/auth/preferences/`
- **Permission:** IsAuthenticated
- **Description:** Get current user preferences

**Response Fields:**
```json
{
  "id": "uuid",
  "favorite_genres": "array",
  "preferred_languages": "array",
  "email_notifications": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

#### 9. Update User Preferences (Full Update)
- **URL:** `PUT /api/v1/auth/preferences/`
- **Permission:** IsAuthenticated
- **Description:** Update user preferences (full update)

**Request Fields:**
```json
{
  "favorite_genres": "array",
  "preferred_languages": "array",
  "email_notifications": "boolean"
}
```

**Response:** Same as Get User Preferences

#### 10. Update User Preferences (Partial Update)
- **URL:** `PATCH /api/v1/auth/preferences/`
- **Permission:** IsAuthenticated
- **Description:** Partially update user preferences

**Request Fields:** (all optional)
```json
{
  "favorite_genres": "array (optional)",
  "preferred_languages": "array (optional)",
  "email_notifications": "boolean (optional)"
}
```

**Response:** Same as Get User Preferences

#### 11. Change Password
- **URL:** `POST /api/v1/auth/change-password/`
- **Permission:** IsAuthenticated
- **Description:** Change user password

**Request Fields:**
```json
{
  "old_password": "string (required)",
  "new_password": "string (required)",
  "new_password_confirm": "string (required)"
}
```

**Response Fields:**
```json
{
  "message": "string"
}
```

## Security Features

### JWT Configuration
- **Access Token Lifetime:** 60 minutes
- **Refresh Token Lifetime:** 7 days
- **Token Rotation:** Enabled
- **Blacklist After Rotation:** Enabled
- **Algorithm:** HS256

### Password Validation
- User attribute similarity validation
- Minimum length validation
- Common password validation
- Numeric password validation

### CORS Configuration
- Allowed origins: localhost:3000, 127.0.0.1:3000 (for frontend)
- Credentials allowed
- Standard headers allowed

## Permissions
- **IsOwner:** Custom permission for user objects
- **IsOwnerOrReadOnly:** Custom permission allowing read-only or owner access
- **IsAdminUser:** Custom permission for admin-only access
- **IsAdminOrReadOnly:** Custom permission allowing read-only or admin access

## Validation Rules
- Email must be unique
- Username must be unique
- Password must meet Django's password validation requirements
- Password confirmation must match password
- Old password verification required for password changes

## Database Configuration
- Uses UUID primary keys for all models
- Custom table names (`users`, `user_preferences`)
- Proper foreign key relationships
- JSON fields for array data (genres, languages)

## API Documentation
- Swagger UI available at `/api/docs/`
- ReDoc available at `/api/redoc/`
- OpenAPI schema available at `/api/schema/`

## Files Created/Modified

### New Files Created:
1. `apps/authentication/models.py` - User and UserPreferences models
2. `apps/authentication/managers.py` - Custom user manager
3. `apps/authentication/serializers.py` - All serializers for authentication
4. `apps/authentication/views.py` - All API views
5. `apps/authentication/permissions.py` - Custom permissions
6. `apps/authentication/urls.py` - URL routing
7. `apps/authentication/admin.py` - Admin configuration
8. `requirements.txt` - Project dependencies
9. `.env.example` - Environment variables template
10. `utils/__init__.py` - Utils module initialization

### Modified Files:
1. `movieexplained_backend/settings.py` - Added all necessary configurations
2. `movieexplained_backend/urls.py` - Added API endpoints and documentation
3. `apps/authentication/apps.py` - Updated app configuration

## Next Steps for Stage 2
After Stage 1 completion, the next stage would typically include:
1. Movies App (3.2.2) - Movie data management
2. Content App (3.2.3) - Movie explanations and blog posts
3. AI Integration App (3.2.4) - Content generation
4. Recommendations App (3.2.5) - Movie recommendations
5. Analytics App (3.2.6) - User analytics and feedback
6. Admin Dashboard App (3.2.7) - Administrative interface
