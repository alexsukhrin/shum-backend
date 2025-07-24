# Shum Marketplace API Usage

## 🚀 API Documentation

**Swagger UI**: http://localhost:8000/api/docs/
**OpenAPI Schema**: http://localhost:8000/api/schema/

## 🔐 Authentication Endpoints

### User Registration
**POST** `/api/auth/register/`

```json
{
  "first_name": "Alexandr",
  "last_name": "Sukhryn",
  "email": "alexandrvirtual@gmail.com",
  "password": "password1986"
}
```

**Response (201):**
```json
{
  "user": {
    "id": 1,
    "email": "alexandrvirtual@gmail.com",
    "first_name": "Alexandr",
    "last_name": "Sukhryn",
    "name": "Alexandr Sukhryn"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

### User Login
**POST** `/api/auth/login/`

```json
{
  "email": "alexandrvirtual@gmail.com",
  "password": "password1986"
}
```

**Response (200):**
```json
{
  "user": {
    "id": 1,
    "email": "alexandrvirtual@gmail.com",
    "first_name": "Alexandr",
    "last_name": "Sukhryn",
    "name": "Alexandr Sukhryn"
  },
  "tokens": {
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

### Token Refresh
**POST** `/api/auth/token/refresh/`

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Token Verify
**POST** `/api/auth/token/verify/`

```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Enhanced Token Obtain
**POST** `/api/auth/token/`

Same as login but with standard JWT format + user data.

## 👤 User Endpoints

### Get Profile
**GET** `/api/auth/profile/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
  "id": 1,
  "email": "alexandrvirtual@gmail.com",
  "first_name": "Alexandr",
  "last_name": "Sukhryn",
  "name": "Alexandr Sukhryn",
  "url": "http://localhost:8000/api/users/1/"
}
```

### Get Current User
**GET** `/api/users/me/`

**Headers:**
```
Authorization: Bearer <access_token>
```

## 🧪 Testing Examples

### Using curl:

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "securepass123"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepass123"
  }'

# Get Profile (replace TOKEN with your access token)
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer TOKEN"
```

### Using JavaScript/Fetch:

```javascript
// Register
const registerResponse = await fetch('/api/auth/register/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    first_name: 'John',
    last_name: 'Doe',
    email: 'john@example.com',
    password: 'securepass123'
  })
});

const userData = await registerResponse.json();
const accessToken = userData.tokens.access;

// Get Profile
const profileResponse = await fetch('/api/auth/profile/', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});

const profile = await profileResponse.json();
```

## 🔑 JWT Token Information

- **Access Token Lifetime**: 60 minutes
- **Refresh Token Lifetime**: 7 days
- **Token Type**: Bearer
- **Header Format**: `Authorization: Bearer <token>`

## 📊 Response Formats

### Success Response
All successful responses return JSON with appropriate HTTP status codes (200, 201, etc.)

### Error Response
```json
{
  "field_name": ["Error message"],
  "non_field_errors": ["General error message"]
}
```

### Authentication Error
```json
{
  "detail": "Authentication credentials were not provided."
}
```

## 🏷️ API Tags in Swagger

- **Authentication**: User registration, login, JWT management
- **Users**: User profile and management operations

## 🔧 Development

- **API Base URL**: http://localhost:8000/api/
- **Swagger UI**: http://localhost:8000/api/docs/
- **Admin Panel**: http://localhost:8000/admin/

## 🌟 Features

✅ JWT Authentication with refresh tokens
✅ User registration with first_name/last_name
✅ Comprehensive Swagger documentation
✅ OpenAPI 3.0 schema
✅ JWT integration in Swagger UI
✅ Detailed request/response examples
✅ Public access to documentation
✅ Pre-commit hooks for code quality
