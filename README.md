# Document Management System (DMS) API

A secure document management system built with Django REST Framework.

## Tech Stack

- **Backend**: Django 4.2 + Django REST Framework
- **Database**: PostgreSQL
- **Cache**: Redis
- **Storage**: MinIO (Object Storage)
- **Task Queue**: Celery
- **Real-time**: Django Channels (WebSocket)
- **Docs**: Swagger UI

## Features

- JWT Authentication
- Role-Based Access Control (RBAC)
  - `admin`: Full access
  - `editor`: Upload and update documents
  - `viewer`: Read only
- Secure document URLs (MinIO presigned URLs)
- Background task processing (Celery)
- Audit logging
- WebSocket notifications
- Filter and Pagination
- Swagger API documentation
- SOLID principles
- Unit Tests

## Project Structure

api-challenge-backend-sanaap/
├── config/          # Project settings
├── users/           # Authentication and RBAC
├── documents/       # Document management
├── audit/           # Audit logging
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/api-challenge-backend-sanaap.git
cd api-challenge-backend-sanaap
```

### 2. Setup environment variables

```bash
cp .env.example .env
# Edit .env with your values
```

### 3. Start infrastructure services

```bash
docker-compose up -d
```

### 4. Install dependencies

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create superuser

```bash
python manage.py createsuperuser
# Then set role to admin via shell:
python manage.py shell
>>> from users.models import User
>>> u = User.objects.get(username='YOUR_USERNAME')
>>> u.role = 'admin'
>>> u.save()
```

### 7. Start Celery worker (new terminal)

```bash
celery -A config worker --loglevel=info
```

### 8. Run server

```bash
python manage.py runserver
```

## API Documentation

Swagger UI: `http://localhost:8000/swagger/`

### Authentication

1. POST `/api/login/` with username and password
2. Copy `swagger_token` from response
3. Click **Authorize** in Swagger and paste the token

### Endpoints

| Method | Endpoint | Role | Description |
|--------|----------|------|-------------|
| POST | `/api/login/` | Public | Get JWT token |
| GET | `/api/documents/` | All | List documents |
| POST | `/api/documents/upload/` | Admin, Editor | Upload single document |
| POST | `/api/documents/batch-upload/` | Admin, Editor | Upload multiple documents |
| GET | `/api/documents/<id>/` | All | Get document |
| PATCH | `/api/documents/<id>/update/` | Admin, Editor | Update document |
| DELETE | `/api/documents/<id>/delete/` | Admin | Delete document |
| POST | `/api/users/create/` | Admin | Create user |
| GET | `/api/users/` | Admin | List users |
| GET | `/api/audit/` | Admin | Audit logs |

### Filtering
GET /api/documents/?status=stored
GET /api/documents/?title=report
GET /api/documents/?page=2
## Environment Variables

```env
DEBUG=True/False
SECRET_KEY=your-secret-key

DB_NAME=dms_db
DB_USER=dms_user
DB_PASSWORD=dms_password
DB_HOST=localhost
DB_PORT=5432

REDIS_URL=redis://localhost:6379/0

MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123
MINIO_BUCKET_NAME=documents
MINIO_SECURE=False
```

## WebSocket

Connect to real-time document notifications:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/documents/');
ws.onmessage = (event) => console.log(JSON.parse(event.data));
```

## Running Tests

```bash
python manage.py test
```

## Git Flow
main        ← production
develop     ← development
feature/*   ← new features
hotfix/*    ← bug fixes

