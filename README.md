# AI Notes & Translation Microservice

A Django-based REST API microservice for managing text notes with automatic translation capabilities. This service allows users to create, store, and translate notes in multiple languages, with built-in caching and analytics.

## Project Overview

This microservice provides a complete backend solution for note management with translation features. Users can:

- Create and manage text notes (via JSON or file upload)
- Translate notes to different languages using Google Translate API
- View analytics and statistics about notes and translations
- Access cached data for improved performance
- Secure API access with JWT authentication

The system is designed with scalability in mind, using Redis for caching and PostgreSQL for persistent storage. All operations are exposed through RESTful APIs with JWT authentication, proper error handling, and pagination.

## Tech Stack

### Backend
- **Python 3.11** - Programming language
- **Django 5.0+** - Web framework
- **Django REST Framework** - API framework
- **PostgreSQL 15** - Relational database
- **Redis 7** - Caching layer
- **JWT Authentication** - Secure API access (djangorestframework-simplejwt)
- **googletrans** - Translation service

### DevOps & Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Service orchestration
- **AWS EC2/EKS** - Cloud deployment (ready)

### Development Tools
- **python-decouple** - Environment variable management
- **psycopg2** - PostgreSQL adapter

## Setup Instructions

### Prerequisites
- Docker and Docker Compose installed
- Git (for cloning the repository)

### Quick Start with Docker (Recommended)

This is the easiest way to get started. Everything runs in containers.

1. **Clone the repository**
   ```bash
   git clone https://github.com/techaneesh/AI-Notes-Translation-Microservice.git
   cd AI-Notes-Translation-Microservice
   ```

2. **Start all services**
   ```bash
   docker compose up --build
   ```

   This will start:
   - PostgreSQL database (port 5435)
   - Redis cache (port 6379)
   - Django web server (port 8005)

3. **Create a superuser** (for authentication)
   ```bash
   docker compose exec web python manage.py createsuperuser
   ```
   Follow the prompts to create your admin user.

4. **Access the API**
   - API Base URL: `http://localhost:8005/api/`
   - Admin Panel: `http://localhost:8005/admin/`
   - **Note:** All API endpoints require JWT authentication (see API Documentation below)

5. **Stop services**
   ```bash
   docker compose down
   ```

### Local Development Setup

If you prefer running without Docker:

1. **Install Python 3.11+** and create a virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   cd ai_notes_translation
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Set up PostgreSQL and Redis**
   - Install and start PostgreSQL locally
   - Install and start Redis locally
   - Update `.env` with local connection details

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (for authentication)
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

### AWS Deployment

#### Option 1: EC2 Deployment

1. **Launch an EC2 instance**
   - Use Ubuntu 22.04 LTS
   - Security group: Allow ports 22 (SSH), 8005 (HTTP), 5435 (PostgreSQL)
   - Minimum: t2.micro (for testing)

2. **SSH into the instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install Docker and Docker Compose**
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose -y
   sudo usermod -aG docker $USER
   # Log out and back in
   ```

4. **Clone and deploy**
   ```bash
   git clone https://github.com/techaneesh/AI-Notes-Translation-Microservice.git
   cd AI-Notes-Translation-Microservice
   docker compose up -d
   ```

## API Documentation

All endpoints return JSON responses. Base URL: `http://localhost:8005/api/`

**⚠️ Important:** All API endpoints require JWT authentication. You must obtain a token first (see Authentication section below).

### Authentication Endpoints

#### Get Access Token (Login)
```bash
curl -X POST http://localhost:8005/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "password": "your_password"
  }'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Access Token
```bash
curl -X POST http://localhost:8005/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }'
```

**Using the Token:**
Include the access token in the Authorization header for all API requests:
```bash
curl -X GET http://localhost:8005/api/notes/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Notes Endpoints

**Note:** All endpoints below require the `Authorization: Bearer <token>` header.

#### Create a Note
```bash
curl -X POST http://localhost:8005/api/notes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{
    "title": "My First Note",
    "text": "This is a sample note text.",
    "original_language": "en"
  }'
```

#### Upload Note from File
```bash
curl -X POST http://localhost:8005/api/notes/upload/ \
  -H "Authorization: Bearer <your_access_token>" \
  -F "file=@note.txt" \
  -F "title=My Note" \
  -F "original_language=en"
```

#### List All Notes
```bash
curl -X GET http://localhost:8005/api/notes/ \
  -H "Authorization: Bearer <your_access_token>"
```

#### Get Single Note
```bash
curl -X GET http://localhost:8005/api/notes/1/ \
  -H "Authorization: Bearer <your_access_token>"
```

#### Update Note
```bash
curl -X PATCH http://localhost:8005/api/notes/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{"title": "Updated Title"}'
```

#### Delete Note
```bash
curl -X DELETE http://localhost:8005/api/notes/1/ \
  -H "Authorization: Bearer <your_access_token>"
```

#### Translate Note
```bash
curl -X POST http://localhost:8005/api/notes/1/translate/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_access_token>" \
  -d '{"target_language": "hi"}'
```

### Analytics Endpoints

#### Get Statistics
```bash
curl -X GET http://localhost:8005/api/stats/ \
  -H "Authorization: Bearer <your_access_token>"
```

Response:
```json
{
  "total_notes": 10,
  "translations_count": 7,
  "breakdown_by_language": {
    "en": 5,
    "hi": 3,
    "es": 2
  }
}
```

#### Check Cache Info (Redis Demo)
```bash
curl -X GET http://localhost:8005/api/cache-info/ \
  -H "Authorization: Bearer <your_access_token>"
```

### Postman Collection

You can import these endpoints into Postman. All endpoints support:
- JSON request/response format
- Proper HTTP status codes
- Error messages in JSON format
- JWT authentication (Bearer token)

**Postman Setup Tips:**
1. Create a Postman environment
2. After login, save tokens in environment variables:
   - `access_token` - Use in Authorization header
   - `refresh_token` - Use for token refresh
3. Set Authorization type to "Bearer Token" and use `{{access_token}}`

For detailed API documentation, see [API_ENDPOINTS.md](ai_notes_translation/API_ENDPOINTS.md)

## Architecture

> **Note**: The HLD and LLD diagrams below were created using [Mermaid](https://mermaid.live/). The source files (`HLD.mmd` and `LLD.mmd`) are available in the root directory of this project. Only need to copy below code and paste in mermaid website.

### High-Level Design (HLD)

```mermaid
graph TB
    subgraph "Client Layer"
        Client[Client Application<br/>Browser/Mobile/Postman]
    end
    
    subgraph "API Layer"
        API[Django REST Framework<br/>Port 8005]
        Auth[JWT Authentication<br/>Token Validation]
    end
    
    subgraph "Application Layer"
        Notes[Notes App<br/>CRUD Operations]
        Analytics[Analytics App<br/>Statistics]
        CacheLayer[Cache Layer<br/>Redis Integration]
    end
    
    subgraph "Data Layer"
        DB[(PostgreSQL Database<br/>Port 5435)]
        Redis[(Redis Cache<br/>Port 6379)]
    end
    
    subgraph "External Services"
        Translate[Google Translate API<br/>Translation Service]
    end
    
    Client -->|HTTP/REST API| API
    API -->|Validate Token| Auth
    Auth -->|Authenticated| Notes
    Auth -->|Authenticated| Analytics
    Notes -->|Read/Write| DB
    Notes -->|Cache Operations| Redis
    Notes -->|Translation Request| Translate
    Analytics -->|Query Data| DB
    Analytics -->|Cache Stats| Redis
    CacheLayer -->|Manage Cache| Redis
    
    style Client fill:#e1f5ff
    style API fill:#fff4e1
    style Auth fill:#ffe1f5
    style Notes fill:#e1ffe1
    style Analytics fill:#e1ffe1
    style DB fill:#ffe1e1
    style Redis fill:#ffe1e1
    style Translate fill:#f5e1ff
```

**Components:**
- **Client Layer**: Browser, mobile apps, or API clients (Postman) making HTTP requests
- **API Layer**: Django REST Framework handles all HTTP requests on port 8005
- **Authentication Layer**: JWT-based authentication secures all endpoints
- **Application Layer**: Notes and Analytics apps contain core business logic
- **Data Layer**: PostgreSQL (port 5435) for persistence, Redis (port 6379) for caching
- **External Service**: Google Translate API for translation functionality

### Low-Level Design (LLD)

#### Request Flow for Translation

```mermaid
sequenceDiagram
    participant Client
    participant API as Django API
    participant Auth as JWT Auth
    participant Cache as Redis Cache
    participant DB as PostgreSQL
    participant Translate as Google Translate
    
    Note over Client,Translate: Translation Request Flow
    
    Client->>API: POST /api/notes/1/translate/<br/>{target_language: "hi"}<br/>Authorization: Bearer token
    API->>Auth: Validate JWT Token
    alt Token Invalid
        Auth-->>API: 401 Unauthorized
        API-->>Client: 401 Unauthorized
    else Token Valid
        Auth-->>API: Token Valid
        API->>Cache: Check cache<br/>key: translation_1_hi
        alt Cache Hit
            Cache-->>API: Return cached translation
            API->>DB: Update note with translation
            DB-->>API: Note updated
            API-->>Client: Return translation (cached: true)
        else Cache Miss
            Cache-->>API: Cache miss
            API->>DB: Fetch note data
            DB-->>API: Note data
            API->>Translate: Translate text<br/>(en → hi)
            Translate-->>API: Translated text
            API->>DB: Save translation to database
            DB-->>API: Translation saved
            API->>Cache: Cache translation<br/>(TTL: 1 hour)
            Cache-->>API: Cached
            API-->>Client: Return translation (cached: false)
        end
    end
```

#### Caching Strategy

- **Notes List**: Cached for 5 minutes, invalidated on create/update/delete
- **Individual Notes**: Cached for 5 minutes, invalidated on update/delete
- **Translations**: Cached for 1 hour (longer TTL due to stable nature)
- **Cache Keys**: Namespaced with `notes_cache:` prefix

#### Database Schema

```
Note Model:
- id (Primary Key)
- title (CharField, max 200)
- text (TextField)
- original_language (CharField, max 10)
- translated_text (TextField, nullable)
- translated_language (CharField, nullable)
- created_at (DateTime)
- updated_at (DateTime)
```

## Design Decisions

### Why PostgreSQL?

I chose PostgreSQL for several reasons:

1. **Relational Data**: Notes have clear relationships and benefit from ACID transactions
2. **Query Flexibility**: Complex analytics queries are easier with SQL
3. **Cost**: PostgreSQL is more relevant for this use case
4. **Familiarity**: My experience in Debuging and maintain
5. **Django Integration**: Excellent ORM support for Django
6. **Scalability**: Can handle significant load, and can migrate to managed services (RDS) when needed

### Caching Approach

I chose Redis for caching instead of storing data in memory. Here's what I did:

- When you create, update, or delete a note, I clear the related cache so you always see fresh data
- Each cached item expires automatically after some time (like 5 minutes for notes, 1 hour for translations)
- When someone requests a translation, I save it in Redis so the next person asking for the same translation gets it instantly

**Why Redis?**
- If the server restarts, the cache doesn't disappear (unlike in-memory cache)
- If you run multiple servers, they can all share the same Redis cache
- It's much faster when lots of people are using the app at the same time
- It's a common industry practice for building scalable applications

### Microservice Architecture

The project is structured as a modular monolith with clear separation:
- **Notes App**: Handles all note-related operations
- **Analytics App**: Handles statistics and reporting
- Each app is self-contained and could be extracted into separate services if needed

This approach provides:
- Clear code organization
- Easy to test and maintain
- Room for future scaling
- Follows Django best practices

### Environment Variables

All sensitive configuration is managed through environment variables:
- Database credentials
- Redis connection details
- Secret keys
- Debug settings

This makes the application:
- Secure (no hardcoded secrets)
- Flexible (easy to change per environment)
- Deployment-ready (works with Docker, AWS, etc.)

### JWT Authentication

**Implementation:**
- JWT-based authentication using `djangorestframework-simplejwt`
- All API endpoints require valid JWT token
- Access tokens expire after 1 hour
- Refresh tokens expire after 7 days
- Token rotation enabled for security

**Why JWT:**
- Stateless authentication (no server-side sessions)
- Scalable across multiple instances
- Industry standard for REST APIs
- Secure token-based access
- Better than session-based auth for microservices

## Known Limitations

1. **Translation Service**: Currently uses free Google Translate API which has rate limits. For production, consider:
   - Paid Google Cloud Translation API
   - Alternative translation services
   - Self-hosted translation models

2. **File Upload Size**: Limited to 5MB for `.txt` files. Large files should be handled differently.

3. **User Management**: Currently uses Django's built-in User model. For production, consider:
   - Custom user model with additional fields
   - User registration API endpoint
   - User profile management
   - Role-based permissions

4. **Testing**: Unit and integration tests are not included. Should add:
   - Test coverage for all endpoints
   - Integration tests for translation flow
   - Cache testing

## Next Steps

### Short Term
- [ ] Add comprehensive test suite
- [ ] Add request rate limiting
- [ ] Set up application logging
- [ ] Create Kubernetes manifests for EKS deployment
- [ ] Add user registration API endpoint

### Medium Term
- [ ] Implement Celery for async translation processing
- [ ] Add monitoring with Prometheus/Grafana or CloudWatch
- [ ] Set up CI/CD pipeline with GitHub Actions
- [ ] Add API versioning
- [ ] Implement GraphQL endpoint (optional)

### Long Term
- [ ] Multi-language support improvements
- [ ] Batch translation operations
- [ ] Translation history/versioning
- [ ] User management and permissions
- [ ] API documentation with Swagger/OpenAPI

---

**Note**: This project was built as part of a microservice architecture assignment. It demonstrates REST API design, JWT authentication, caching strategies, database design, and containerization with Docker.
