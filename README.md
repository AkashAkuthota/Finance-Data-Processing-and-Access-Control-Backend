# Finance Data Processing & Access Control Backend (FastAPI)

A FastAPI-based backend system for managing financial records with **role-based access control (RBAC)**. This project demonstrates clean backend architecture, secure authentication, and dashboard analytics.

---

## 🚀 Live API

- **Base URL:**  
  https://finance-data-processing-and-access-vywg.onrender.com

- **Swagger Docs (Test APIs):**  
  https://finance-data-processing-and-access-vywg.onrender.com/docs

⚠️ Note:  
Authentication is required for protected endpoints. Use `/auth/login` to obtain an access token.

## 🚀 Features

### 🔐 Authentication & Security

* JWT-based authentication (access tokens)
* Refresh tokens stored securely in **HTTPOnly cookies**
* **Refresh token rotation**
* **Reuse detection** (revokes all sessions if a revoked token is reused)
* Token blacklisting (Redis) for logout
* Rate limiting to prevent abuse

---

### 👤 User & Role Management

* User registration and login
* Role-based access control:

  * **Viewer** → dashboard only
  * **Analyst** → read records + analytics
  * **Admin** → full access
* User activation/deactivation
* Role assignment (admin only)

---

### 💰 Financial Records Management

* Create, read, update, delete financial records
* **Soft delete** (records are marked as deleted)
* Filtering:

  * type (income/expense)
  * category
  * date range
* Pagination support
* Fields:

  * amount
  * type
  * category
  * date
  * description

---

### 📊 Dashboard Analytics

* Total income, expenses, net balance
* Category-wise breakdown
* Recent transactions
* Monthly trends

---

### ⚙️ Additional Enhancements

* Redis-based rate limiting
* Structured logging for monitoring
* Input validation using Pydantic
* Clean error handling with proper HTTP responses

---

## 🧱 Tech Stack

* **Framework**: FastAPI
* **Database**: PostgreSQL + SQLAlchemy ORM
* **Authentication**: JWT (python-jose)
* **Password Hashing**: bcrypt (passlib)
* **Cache / Blacklist**: Redis
* **Validation**: Pydantic
* **Logging**: Python logging module

---

## 📁 Project Structure

```
app/
├── core/
│   ├── config.py          # Application settings & environment config
│   ├── dependencies.py    # Auth dependencies & role checking
│   ├── security.py        # Password hashing & JWT functions
│   └── __init__.py
├── db/
│   ├── base.py           # SQLAlchemy base configuration
│   ├── session.py        # Database session management
│   └── __init__.py
├── models/
│   ├── user.py           # User model with relationships
│   ├── role.py           # Role model definitions
│   ├── financial_record.py # Financial record model
│   ├── refresh_token.py  # Token model for rotation
│   └── __init__.py
├── routes/
│   ├── auth_routes.py    # Authentication endpoints
│   ├── user_routes.py    # User management endpoints
│   ├── finance_routes.py # Financial records CRUD
│   ├── dashboard_routes.py # Analytics endpoints
│   └── __init__.py
├── schemas/
│   ├── auth.py           # Auth request/response models
│   ├── user.py           # User validation schemas
│   ├── financial_record.py # Record validation schemas
│   └── __init__.py
├── services/
│   ├── auth_service.py   # Authentication business logic
│   ├── user_service.py   # User management logic
│   ├── finance_service.py # Record operations & search
│   ├── dashboard_service.py # Analytics calculations
│   └── __init__.py
└── utils/
    ├── rate_limiter.py   # Rate limiting implementation
    ├── redis_client.py   # Redis connection utilities
    ├── token_blacklist.py # Token management
    └── __init__.py
```

* **Routes** → API layer with endpoint definitions
* **Services** → Business logic and data processing
* **Models** → Database schema and relationships
* **Schemas** → Request/response validation models

---

## ⚡ Quick Test Flow (Important)

1. **Signup**

```
POST /users/signup
```

2. **Login**

```
POST /auth/login
```

3. **Promote user to admin**

```
PATCH /users/{user_id}/role?role=admin
```

4. **Create records**

```
POST /records/
```

5. **Check dashboard**

```
GET /dashboard/summary
```

---

## 🔐 Authentication Flow

### Login

```json
{
  "access_token": "jwt_token"
}
```

* Refresh token is stored securely in an **HTTPOnly cookie**

---

### Refresh

```
POST /auth/refresh
```

* Reads refresh token from cookie
* Rotates token
* Returns new access token

---

### Logout

```
POST /auth/logout
```

* Revokes refresh token
* Blacklists access token
* Clears cookie

---

## 🔒 Role-Based Access Control

| Endpoint        | Viewer | Analyst | Admin |
| --------------- | ------ | ------- | ----- |
| Dashboard       | ✅      | ✅       | ✅     |
| Records (GET)   | ❌      | ✅       | ✅     |
| Records (CRUD)  | ❌      | ❌       | ✅     |
| User Management | ❌      | ❌       | ✅     |

Access control is enforced using **dependency-based role guards** at the backend level.

---

## ⚙️ Setup Instructions

### 1. Clone & Setup

```bash
git clone <repo_url>
cd finance-backend
python -m venv venv
source venv/bin/activate
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Configure Environment

Create `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=finance_db
DB_USER=postgres
DB_PASSWORD=your_password

SECRET_KEY=your_secret
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

REDIS_URL=redis://localhost:6379
ENVIRONMENT=development
```

---

### 4. Run Server

```bash
uvicorn app.main:app --reload
```

---

## 🧠 Assumptions

* Default role is **viewer**
* PostgreSQL used for persistence
* Redis used for rate limiting and token blacklist
* Offset-based pagination

---

## 🔐 Security Highlights

* Password hashing using bcrypt
* JWT authentication
* HTTPOnly cookies for refresh tokens
* Token rotation + reuse detection
* Redis-based rate limiting and token blacklist

---

## 🚀 Deployment (Optional)

Recommended stack:

* PostgreSQL → Neon
* Redis → Upstash
* Backend → Render

---

## 📌 Project Highlights

### ✅ Core Requirements

* User & role management
* Financial record CRUD
* Dashboard analytics
* Access control (RBAC)
* Validation & error handling
* Data persistence

---

### 🚀 Enhancements

* Secure refresh token handling (cookie-based)
* Token rotation & reuse detection
* Rate limiting
* Logging
* Clean modular architecture

---

## 🧾 Conclusion

This project demonstrates a **production-oriented backend design** with secure authentication, clean architecture, and scalable data handling. It balances simplicity with practical enhancements to reflect real-world backend engineering practices.
