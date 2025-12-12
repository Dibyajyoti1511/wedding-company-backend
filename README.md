# Wedding Company Organization Management Service

A comprehensive backend service for managing wedding companies with multi-tenant architecture, built with FastAPI and MongoDB.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Authentication](#authentication)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This service provides a robust backend solution for wedding companies to manage multiple organizations in a multi-tenant architecture. Each organization gets its own isolated database space while maintaining centralized authentication and metadata management.

The system implements RESTful APIs for organization CRUD operations, admin authentication, and wedding event management, making it suitable for wedding planning businesses that need to scale across multiple clients.

## ✨ Features

### Core Organization Management
- ✅ **Multi-tenant Architecture**: Isolated data per organization
- ✅ **Dynamic Database Creation**: Automatic MongoDB collection creation per organization
- ✅ **Organization CRUD**: Create, read, update, and delete organizations
- ✅ **Admin Authentication**: JWT-based authentication system
- ✅ **Secure Password Hashing**: bcrypt encryption for admin passwords

### Wedding Management (Bonus Features)
- ✅ **Wedding CRUD Operations**: Complete wedding event management
- ✅ **Flexible Schema**: Extensible wedding data structure
- ✅ **Organization-scoped Data**: All wedding data isolated per organization

### Technical Features
- ✅ **RESTful API Design**: Clean, intuitive endpoints
- ✅ **Error Handling**: Comprehensive error responses
- ✅ **Input Validation**: Pydantic-based request validation
- ✅ **Modular Architecture**: Clean separation of concerns
- ✅ **Type Safety**: Full type hints throughout the codebase

## 🛠 Tech Stack

### Backend Framework
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.14** - Programming language

### Database
- **MongoDB** - NoSQL database for flexible data storage
- **PyMongo** - MongoDB driver for Python

### Authentication & Security
- **PyJWT** - JSON Web Token implementation
- **PassLib** - Password hashing library
- **bcrypt** - Secure password hashing algorithm

### Validation & Settings
- **Pydantic** - Data validation and settings management
- **Pydantic-Settings** - Environment-based configuration
- **Email-Validator** - Email validation

### Development Tools
- **Uvicorn** - ASGI server for FastAPI
- **Python-dotenv** - Environment variable management

## 🏗 Architecture

### System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │────│   Services      │────│  Repositories   │
│                 │    │                 │    │                 │
│ • Routers       │    │ • OrgService    │    │ • MasterRepo    │
│ • Middleware    │    │ • AuthService   │    │ • OrgRepo       │
│ • Error Handling│    │ • WeddingService│    └─────────────────┘
└─────────────────┘    └─────────────────┘             │
                        │                            │
                        └────────────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   MongoDB       │
                    │                 │
                    │ • Master DB     │
                    │   • orgs        │
                    │   • admins      │
                    │                 │
                    │ • Org DBs       │
                    │   • org_org1    │
                    │   • org_org2    │
                    │   • ...         │
                    └─────────────────┘
```

### Database Architecture

**Master Database** (`master_db`):
- Stores global metadata and admin credentials
- Contains organization registry and admin user data

**Organization Databases** (`org_<organization_name>`):
- Dynamic collections created per organization
- Isolated data storage for organization-specific information

## 🚀 Installation

### Prerequisites

- Python 3.14 or higher
- MongoDB (local or cloud instance)
- Git

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd wedding-company-service
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   ```bash
   # Windows
   .venv\Scripts\activate

   # Linux/Mac
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Start MongoDB**
   ```bash
   # If using local MongoDB
   mongod

   # Or ensure your MongoDB instance is running
   ```

## ⚙️ Configuration

### Environment Variables (.env)

```env
# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017
MASTER_DB_NAME=master_db

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXP_HOURS=3

# Optional: Email validation settings
# EMAIL_VALIDATOR_DNS_RESOLVER=1.1.1.1
```

### Configuration Details

- **MONGO_URI**: MongoDB connection string
- **MASTER_DB_NAME**: Name of the master database
- **JWT_SECRET**: Secret key for JWT token signing (change in production!)
- **JWT_ALGORITHM**: JWT algorithm (HS256 recommended)
- **JWT_EXP_HOURS**: Token expiration time in hours

## 📖 Usage

### Starting the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### API Base URL
```
http://localhost:8000
```

### Interactive API Documentation
Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Documentation

### Authentication Endpoints

#### POST /admin/login
Admin authentication endpoint.

**Request Body:**
```json
{
  "email": "admin@organization.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Organization Management Endpoints

#### POST /org/create
Create a new organization.

**Request Body:**
```json
{
  "organization_name": "DreamWeddings",
  "email": "admin@dreamweddings.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "organization_name": "DreamWeddings",
    "collection_name": "org_DreamWeddings",
    "admin_id": "507f1f77bcf86cd799439011"
  }
}
```

#### GET /org/get?organization_name=DreamWeddings
Get organization details.

**Response:**
```json
{
  "success": true,
  "data": {
    "organization_name": "DreamWeddings",
    "collection_name": "org_DreamWeddings",
    "admin_id": "..."
  }
}
```

#### PUT /org/update
Update organization details.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "organization_name": "DreamWeddings",
  "new_organization_name": "DreamWeddingsPro",
  "email": "newadmin@dreamweddings.com",
  "password": "newpassword"
}
```

#### DELETE /org/delete?organization_name=DreamWeddings
Delete an organization.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

### Wedding Management Endpoints (Bonus)

#### POST /weddings/
Create a wedding event.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

**Request Body:**
```json
{
  "bride_name": "Sarah Johnson",
  "groom_name": "Michael Smith",
  "wedding_date": "2025-06-15",
  "venue": "Grand Ballroom Hotel",
  "budget": 50000.00
}
```

#### GET /weddings/
List all weddings for the organization.

**Headers:**
```
Authorization: Bearer <jwt_token>
```

#### GET /weddings/{wedding_id}
Get specific wedding details.

#### PUT /weddings/{wedding_id}
Update wedding information.

#### DELETE /weddings/{wedding_id}
Delete a wedding event.

## 🗄️ Database Schema

### Master Database Collections

#### organizations (orgs)
```javascript
{
  _id: ObjectId,
  organization_name: String,
  collection_name: String, // "org_<organization_name>"
  admin_id: ObjectId,
  created_at: Date
}
```

#### admins
```javascript
{
  _id: ObjectId,
  email: String,
  password: String, // bcrypt hashed
  organization: String,
  created_at: Date
}
```

### Organization Database Collections

#### data (weddings and other org-specific data)
```javascript
{
  _id: ObjectId,
  type: String, // "wedding", "client", etc.
  organization: String,
  // Wedding-specific fields
  bride_name: String,
  groom_name: String,
  wedding_date: String,
  venue: String,
  budget: Number,
  // Additional fields as needed
  created_at: Date,
  updated_at: Date
}
```

## 🔐 Authentication

### JWT Token Structure
```json
{
  "admin_id": "507f1f77bcf86cd799439011",
  "organization": "DreamWeddings",
  "exp": 1640995200
}
```

### Authentication Flow
1. Admin logs in with email/password
2. Server validates credentials against master database
3. JWT token is generated with admin ID and organization
4. Client includes token in Authorization header for protected routes
5. Server validates token and extracts organization context

### Security Features
- Password hashing with bcrypt
- JWT token expiration (configurable)
- Organization-scoped data access
- Input validation and sanitization

## 🧪 Testing

### Running Tests
```bash
# Install test dependencies if any
pip install pytest

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

### Test Structure
```
tests/
├── test_org_endpoints.py
├── test_auth_endpoints.py
├── test_wedding_endpoints.py
├── conftest.py
└── test_data.py
```

### Manual Testing with cURL

```bash
# Create organization
curl -X POST "http://localhost:8000/org/create" \
  -H "Content-Type: application/json" \
  -d '{
    "organization_name": "TestOrg",
    "email": "admin@test.com",
    "password": "password123"
  }'

# Login
curl -X POST "http://localhost:8000/admin/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "password123"
  }'
```

## 🚀 Deployment

### Docker Deployment

1. **Create Dockerfile**
```dockerfile
FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Create docker-compose.yml**
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGO_URI=mongodb://mongodb:27017
    depends_on:
      - mongodb

  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

3. **Deploy**
```bash
docker-compose up -d
```

### Production Considerations

- Use environment-specific configuration
- Set strong JWT secrets
- Configure MongoDB authentication
- Set up proper logging
- Implement rate limiting
- Add API versioning
- Set up monitoring and health checks

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Ensure all tests pass
6. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Write descriptive commit messages
- Add docstrings to functions and classes

### Pull Request Guidelines

- Provide clear description of changes
- Include relevant tests
- Update documentation if needed
- Ensure CI/CD passes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For questions or support, please contact the development team or create an issue in the repository.

## 🔄 Future Enhancements

- [ ] Client management system
- [ ] Vendor management
- [ ] Invoice and payment integration
- [ ] Email notifications
- [ ] File upload for wedding photos
- [ ] Calendar integration
- [ ] Mobile app API
- [ ] Advanced reporting and analytics
- [ ] Multi-language support
- [ ] API rate limiting
- [ ] Caching layer (Redis)
- [ ] Background job processing

---

**Built with ❤️ using FastAPI and MongoDB**</content>
<parameter name="filePath">c:\Users\rishi\Desktop\wedding company\README.md