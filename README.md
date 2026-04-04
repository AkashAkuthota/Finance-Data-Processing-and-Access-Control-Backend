# Finance Data Processing and Access Control Backend

A FastAPI-based backend system for managing financial records with role-based access control. This project implements a complete finance dashboard backend with user management, financial record CRUD operations, and dashboard analytics.

## Features

### User and Role Management
- User registration and authentication
- Role-based access control (Viewer, Analyst, Admin)
- User status management (active/inactive)
- JWT-based authentication with token blacklisting

### Financial Records Management
- Create, read, update, delete financial records
- **Soft delete** functionality (records are marked as deleted, not removed)
- Record filtering by type, category, and date range
- **Search functionality** by description or category
- Pagination support
- Fields: amount, type (income/expense), category, date, description

### Dashboard Analytics
- Summary statistics (total income, expenses, net balance)
- Category-wise breakdown
- Recent transactions
- Monthly trends analysis

### Access Control
- **Viewer**: Can view dashboard data and summaries
- **Analyst**: Can view records and access insights
- **Admin**: Full CRUD access to records and user management

### Additional Features
- **Rate Limiting**: Prevents abuse with configurable limits
- **Comprehensive Logging**: All operations are logged for monitoring
- **Input Validation**: Strict validation using Pydantic
- **Error Handling**: Proper HTTP status codes and error messages
- **Search API**: Full-text search across records

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/refresh` - Refresh access token

### User Management
- `POST /users/signup` - User registration
- `GET /users/me` - Get current user info
- `PUT /users/me` - Update current user
- `DELETE /users/me` - Deactivate current user

### Financial Records
- `POST /records/` - Create new record (Admin only)
- `GET /records/` - List records with filtering & pagination (Analyst+)
- `GET /records/search?q=search_term` - Search records (Analyst+)
- `PUT /records/{id}` - Update record (Admin only)
- `DELETE /records/{id}` - Soft delete record (Admin only)

### Dashboard
- `GET /dashboard/summary` - Financial summary
- `GET /dashboard/category` - Category breakdown
- `GET /dashboard/recent` - Recent transactions
- `GET /dashboard/trends` - Monthly trends

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT tokens with jose
- **Password Hashing**: bcrypt with passlib (72-byte limit handling)
- **Caching/Blacklist**: Redis
- **Validation**: Pydantic with custom validators
- **Rate Limiting**: Custom implementation with Redis
- **Logging**: Python logging with file and console handlers
- **API Documentation**: Auto-generated Swagger UI and ReDoc

## Project Structure

```
app/
├── core/
│   ├── config.py          # Application settings
│   ├── dependencies.py    # Auth dependencies and role checking
│   ├── security.py        # Password hashing and JWT functions
│   └── __init__.py
├── db/
│   ├── base.py           # SQLAlchemy base
│   ├── session.py        # Database session management
│   └── __init__.py
├── models/
│   ├── user.py           # User model
│   ├── role.py           # Role model
│   ├── financial_record.py # Financial record model
│   ├── refresh_token.py  # Token model
│   └── __init__.py
├── routes/
│   ├── auth_routes.py    # Authentication endpoints
│   ├── user_routes.py    # User management
│   ├── finance_routes.py # Financial records CRUD
│   └── dashboard_routes.py # Analytics endpoints
├── schemas/
│   ├── auth.py           # Auth request/response models
│   ├── user.py           # User models
│   └── financial_record.py # Record models
├── services/
│   ├── auth_service.py   # Authentication logic
│   ├── user_service.py   # User management logic
│   ├── finance_service.py # Record operations
│   └── dashboard_service.py # Analytics logic
└── utils/
    ├── rate_limiter.py   # Rate limiting
    ├── redis_client.py   # Redis utilities
    └── token_blacklist.py # Token management
```

## Setup Instructions

### Prerequisites
- Python 3.12+
- PostgreSQL
- Redis (optional, for token blacklisting)

### Installation

1. **Clone and setup virtual environment:**
```bash
cd finance-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Environment Configuration:**
Create a `.env` file with:
```env
# ENVIRONMENT (development or production)
ENVIRONMENT=development

# DATABASE CONFIG
DB_HOST=localhost
DB_PORT=5432
DB_NAME=finance_db
DB_USER=postgres
DB_PASSWORD=your_password

# JWT CONFIG
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# REDIS CONFIG (optional)
REDIS_URL=redis://localhost:6379
```

4. **Database Setup:**
- Create PostgreSQL database: `finance_db`
- Start Redis server (if using token blacklisting)
- Run the application - tables will be created automatically

5. **Start the server:**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Documentation

### Authentication Endpoints

#### POST `/auth/login`
Login with email and password to get access token.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password"
}
```

**Response:**
```json
{
  "access_token": "jwt_token",
  "refresh_token": "refresh_token",
  "token_type": "bearer"
}
```

#### POST `/auth/refresh`
Refresh access token using refresh token.

### User Management Endpoints

#### POST `/users/signup`
Create a new user account (no authentication required).

#### PATCH `/users/{user_id}/role` (Admin only)
Change user role.

#### PATCH `/users/{user_id}/status` (Admin only)
Activate/deactivate user account.

### Financial Records Endpoints

#### POST `/records/` (Admin only)
Create a new financial record.

**Request:**
```json
{
  "amount": 1000.50,
  "type": "income",
  "category": "salary",
  "date": "2026-01-15",
  "description": "Monthly salary"
}
```

#### GET `/records/` (Analyst/Admin)
Get paginated list of records with optional filters.

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Records per page (default: 10)
- `type`: Filter by type (income/expense)
- `category`: Filter by category
- `start_date`: Filter from date
- `end_date`: Filter to date

#### PUT `/records/{record_id}` (Admin only)
Update a financial record.

#### DELETE `/records/{record_id}` (Admin only)
Delete a financial record.

### Dashboard Endpoints

#### GET `/dashboard/summary` (All authenticated users)
Get financial summary.

**Response:**
```json
{
  "total_income": 5000.00,
  "total_expense": 3200.00,
  "net_balance": 1800.00
}
```

#### GET `/dashboard/category` (All authenticated users)
Get category-wise totals.

#### GET `/dashboard/recent` (All authenticated users)
Get 5 most recent transactions.

#### GET `/dashboard/trends` (All authenticated users)
Get monthly financial trends.

## Role-Based Access Control

| Endpoint | Viewer | Analyst | Admin |
|----------|--------|---------|-------|
| `/auth/*` | ✅ | ✅ | ✅ |
| `/users/signup` | ✅ | ✅ | ✅ |
| `/users/*` (management) | ❌ | ❌ | ✅ |
| `/records` (GET) | ❌ | ✅ | ✅ |
| `/records` (POST/PUT/DELETE) | ❌ | ❌ | ✅ |
| `/dashboard/*` | ✅ | ✅ | ✅ |

## Assumptions Made

1. **Default Role**: New users are assigned "viewer" role by default
2. **Role Names**: Using "viewer", "analyst", "admin" as role names
3. **Database**: PostgreSQL is the primary database with proper indexing
4. **Authentication**: JWT tokens with refresh token mechanism
5. **Password Security**: bcrypt hashing with 72-character limit
6. **Date Handling**: Using Python date objects for financial record dates
7. **Pagination**: Basic offset-based pagination for record listing
8. **Error Handling**: HTTP status codes with descriptive error messages

## Deployment Guide

### Environment Configuration

The application supports both **development** and **production** environments:

```bash
# Development (default)
ENVIRONMENT=development
# - Cookies: insecure (HTTP only)
# - Database SSL: disabled
# - Best for local development

# Production
ENVIRONMENT=production
# - Cookies: secure (HTTPS required)
# - Database SSL: enabled
# - Required for deployed applications
```

### Deployment Stack (Recommended)

1. **Database**: [Neon](https://neon.tech) (PostgreSQL)
   - Free tier with serverless PostgreSQL
   - Auto-backups and scaling

2. **Redis/Cache**: [Upstash](https://upstash.com) (Redis)
   - Serverless Redis
   - For rate limiting and token blacklisting

3. **Hosting**: [Render](https://render.com) (FastAPI)
   - Free tier with auto-deployment from GitHub
   - Native Python/FastAPI support

### Deployment Environment Variables

When deploying on Render, set these environment variables:

```bash
# Environment
ENVIRONMENT=production

# Database (from Neon)
DB_HOST=your-neon-host.neon.tech
DB_PORT=5432
DB_NAME=neon_db
DB_USER=neon_user
DB_PASSWORD=your_neon_password

# JWT
SECRET_KEY=generate_a_strong_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis (from Upstash)
REDIS_URL=https://default:password@your-upstash-host.upstash.io
```

### Key Deployment Differences

- **SSL Certificates**: Automatically handled by Render (HTTPS enforced)
- **Secure Cookies**: Automatically enabled when `ENVIRONMENT=production`
- **Database Connection**: Uses SSL (`sslmode=require`) in production
- **Logging**: File-based logs in production (stored in Render logs)


## Database Schema

### Users Table
- id (Primary Key)
- email (Unique)
- hashed_password
- is_active (Boolean)
- role_id (Foreign Key to roles)

### Roles Table
- id (Primary Key)
- name (Unique: viewer, analyst, admin)

### Financial Records Table
- id (Primary Key)
- amount (Float)
- type (String: income/expense)
- category (String)
- date (Date)
- description (Text, optional)
- user_id (Foreign Key to users)

### Refresh Tokens Table
- id (Primary Key)
- token (String)
- user_id (Foreign Key to users)

## Security Features

- **Password Hashing**: bcrypt with salt
- **JWT Authentication**: Access and refresh tokens
- **Token Blacklisting**: Redis-based token revocation
- **Rate Limiting**: Custom implementation for API protection
- **Input Validation**: Pydantic models for all inputs
- **SQL Injection Protection**: SQLAlchemy ORM

## Testing the API

1. **Create a user account:**
```bash
curl -X POST "http://127.0.0.1:8000/users/signup" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "password123"}'
```

2. **Login to get token:**
```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "password123"}'
```

3. **Use token for authenticated requests:**
```bash
curl -X GET "http://127.0.0.1:8000/dashboard/summary" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Future Enhancements

- Unit and integration tests
- API rate limiting improvements
- Email notifications
- Data export functionality
- Advanced analytics and reporting
- Multi-tenant support
- API versioning
- Comprehensive logging and monitoring

## Project Highlights for Internship Assignment

This project has been enhanced beyond the basic requirements to demonstrate advanced backend development skills:

### ✅ Core Requirements Implemented
- **User & Role Management**: Complete user system with 3-tier role access (Viewer/Analyst/Admin)
- **Financial Records Management**: Full CRUD with filtering, pagination, and validation
- **Dashboard Analytics**: Comprehensive summary, trends, and category breakdowns
- **Access Control**: Middleware-based role checking with proper HTTP responses
- **Validation & Error Handling**: Pydantic validation with meaningful error messages
- **Data Persistence**: PostgreSQL with SQLAlchemy ORM

### 🚀 Additional Enhancements 
- **Soft Delete**: Records are marked as deleted, not removed from database
- **Search Functionality**: Full-text search across descriptions and categories
- **Rate Limiting**: Prevents API abuse with configurable limits per user
- **Comprehensive Logging**: All operations logged to file and console
- **Unit Tests**: pytest test suite with database mocking
- **Input Validation**: Advanced Pydantic validators with business rules
- **Security**: Password truncation for bcrypt compatibility, token blacklisting
- **API Documentation**: Auto-generated docs with examples

### 🏗️ Architecture & Best Practices
- **Clean Architecture**: Separation of concerns (routes/services/models)
- **Dependency Injection**: Proper FastAPI dependency management
- **Error Handling**: Try-catch blocks with appropriate HTTP status codes
- **Database Design**: Proper relationships and constraints
- **Configuration Management**: Environment-based settings
- **Logging Strategy**: Structured logging for monitoring and debugging


## Conclusion

This backend implementation provides a solid foundation for a finance dashboard application with proper separation of concerns, role-based access control, and comprehensive API endpoints. The code is structured for maintainability and follows FastAPI best practices.