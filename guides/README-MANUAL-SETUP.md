# Manual Server Setup (No Docker)

This guide explains how to run the SaaS MVP without Docker.

## Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL (running on port 5433)
- Redis (running on port 6379)

## Quick Start

### 1. Make scripts executable:

```bash
chmod +x start-*.sh
```

### 2. Start all services at once:

```bash
./start-all.sh
```

This will open separate terminal tabs for:
- Django backend (http://localhost:8000)
- Nuxt frontend (http://localhost:3000)
- Celery worker
- Celery beat scheduler

### Or start services individually:

```bash
# Start Django backend
./start-backend.sh

# Start Nuxt frontend (in another terminal)
./start-frontend.sh

# Start Celery worker (in another terminal)
./start-celery.sh

# Start Celery beat (in another terminal)
./start-celery-beat.sh
```

## Environment Configuration

### Backend (.env)

Edit `backend/.env`:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=saas_mvp
DB_USER=ovsenjak
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5433
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Frontend (.env)

Edit `frontend/.env`:

```
API_BASE_URL=http://localhost:8000/api/v1
```

## Database Setup

If you need to reset the database:

```bash
# Drop and recreate database
psql -U ovsenjak -h localhost -p 5433 -c "DROP DATABASE saas_mvp;" postgres
psql -U ovsenjak -h localhost -p 5433 -c "CREATE DATABASE saas_mvp;" postgres

# Create migrations
./env/bin/python backend/manage.py makemigrations

# Run migrations
./env/bin/python backend/manage.py migrate

# Create superuser (optional)
./env/bin/python backend/manage.py createsuperuser
```

## Useful Commands

### Backend

```bash
# Run Django shell
./env/bin/python backend/manage.py shell

# Collect static files
./env/bin/python backend/manage.py collectstatic

# Create superuser
./env/bin/python backend/manage.py createsuperuser

# Run tests
./env/bin/pytest backend/
```

### Frontend

```bash
# Run in development mode
cd frontend && npm run dev

# Build for production
cd frontend && npm run build

# Preview production build
cd frontend && npm run preview
```

### Celery

```bash
# Monitor Celery tasks
./env/bin/celery -A config inspect active

# Purge all tasks
./env/bin/celery -A config purge

# Monitor with Flower (requires flower package)
./env/bin/celery -A config flower
```

## Troubleshooting

### Port Already in Use

If you get "port already in use" errors:

```bash
# Find process using port 8000
lsof -ti:8000 | xargs kill -9

# Find process using port 3000
lsof -ti:3000 | xargs kill -9
```

### PostgreSQL Connection Issues

Make sure PostgreSQL is running:

```bash
# Check if PostgreSQL is running
pg_isready -h localhost -p 5433
```

### Redis Connection Issues

Make sure Redis is running:

```bash
# Check if Redis is running
redis-cli ping
```

### Python Virtual Environment

If the virtual environment has issues:

```bash
# Recreate virtual environment
rm -rf env
python3.10 -m venv env
./env/bin/pip install -r backend/requirements/development.txt
```

## Development URLs

- Backend API: http://localhost:8000
- Backend Admin: http://localhost:8000/admin
- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/api/schema/swagger-ui/

## Production Deployment

For production deployment without Docker, you should:

1. Use a production WSGI server (Gunicorn):
   ```bash
   ./env/bin/gunicorn config.wsgi:application --bind 0.0.0.0:8000
   ```

2. Build the frontend for production:
   ```bash
   cd frontend && npm run build
   ```

3. Use a process manager like systemd or supervisor to manage services

4. Set up a reverse proxy (Nginx or similar)

5. Configure SSL certificates for HTTPS
