# SaaS MVP - Complete Architecture Guide

A full-stack SaaS application built with Django REST Framework and Nuxt 3, featuring authentication, billing, and deployment-ready configuration.

## 🚀 Tech Stack

- **Backend**: Django 5.0 + Django REST Framework
- **Database**: PostgreSQL
- **Frontend**: Nuxt 3 + Tailwind CSS
- **Email**: Resend
- **Payments**: Stripe (Subscriptions + Credits)
- **Task Queue**: Celery + Redis
- **Auth**: Email/Password + Google OAuth
- **Deployment**: Docker + Nginx

## 📁 Project Structure

```
saas-mvp/
├── backend/                    # Django backend
│   ├── config/                 # Django project settings
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   └── celery.py
│   ├── apps/
│   │   ├── accounts/          # User management
│   │   ├── billing/           # Stripe integration
│   │   └── core/              # Shared utilities
│   ├── requirements/
│   └── manage.py
├── frontend/                   # Nuxt 3 frontend
│   ├── pages/                 # Vue pages
│   ├── components/            # Vue components
│   ├── stores/                # Pinia stores
│   ├── middleware/            # Route middleware
│   └── nuxt.config.ts
├── nginx/                     # Nginx configuration
├── docker-compose.yml         # Docker orchestration
└── README.md
```

## 🏗️ Architecture

The application follows a clean architecture pattern:

**Frontend => REST API (validation) => Service Layer (business logic)**

- **Frontend (Nuxt 3)**: User interface with authentication, dashboard, billing
- **REST API (DRF)**: Data validation, serialization, authentication
- **Service Layer**: Business logic, external API integration, background tasks

## 🛠️ Local Development Setup

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Quick Start with Docker

1. **Clone and setup environment**:
```bash
git clone <your-repo>
cd saas-mvp

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

2. **Configure environment variables**:

Edit `backend/.env`:
```env
SECRET_KEY=your-secret-key-here
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
RESEND_API_KEY=re_...
GOOGLE_CLIENT_ID=...
```

Edit `frontend/.env`:
```env
API_BASE_URL=http://localhost:8000/api/v1
STRIPE_PUBLISHABLE_KEY=pk_test_...
GOOGLE_CLIENT_ID=...
```

3. **Start services**:
```bash
docker-compose up -d
```

4. **Initialize database**:
```bash
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

5. **Access the application**:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

### Local Development (without Docker)

1. **Backend setup**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements/development.txt

# Setup database
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

2. **Frontend setup**:
```bash
cd frontend
npm install
npm run dev
```

3. **Start Redis and Celery**:
```bash
# Terminal 1: Redis
redis-server

# Terminal 2: Celery Worker
cd backend
celery -A config worker -l info

# Terminal 3: Celery Beat (optional, for scheduled tasks)
celery -A config beat -l info
```

## 🚀 Production Deployment

### Ubuntu VPS Deployment

#### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again for docker group to take effect
```

#### 2. Deploy Application

```bash
# Clone repository
git clone <your-repo> /opt/saas-mvp
cd /opt/saas-mvp

# Setup environment
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit environment files with production values
nano backend/.env
nano frontend/.env
```

#### 3. Production Environment Configuration

**backend/.env**:
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
DOMAIN=yourdomain.com
SERVER_IP=your.server.ip

DB_NAME=saas_mvp
DB_USER=postgres
DB_PASSWORD=secure-password

STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

RESEND_API_KEY=re_...
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

SENTRY_DSN=your-sentry-dsn  # Optional
```

#### 4. SSL Certificate Setup

```bash
# Create SSL directory
sudo mkdir -p /opt/saas-mvp/nginx/ssl

# Generate self-signed certificate (replace with real certificate)
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /opt/saas-mvp/nginx/ssl/key.pem \
  -out /opt/saas-mvp/nginx/ssl/cert.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=yourdomain.com"

# For Let's Encrypt (recommended):
# sudo apt install certbot
# sudo certbot certonly --standalone -d yourdomain.com
# sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem /opt/saas-mvp/nginx/ssl/cert.pem
# sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem /opt/saas-mvp/nginx/ssl/key.pem
```

#### 5. Deploy with Docker Compose

```bash
# Start services
docker-compose -f docker-compose.yml up -d

# Initialize database
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py collectstatic --noinput

# Setup Stripe plans (optional)
docker-compose exec backend python manage.py shell
```

#### 6. Configure Firewall

```bash
# Allow SSH, HTTP, HTTPS
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

#### 7. Setup Domain and DNS

1. Point your domain to your server IP
2. Update `DOMAIN` in backend/.env
3. Restart services: `docker-compose restart`

### Docker Production Override

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    environment:
      - DEBUG=0
      - DJANGO_SETTINGS_MODULE=config.settings.production
    command: gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi:application

  frontend:
    environment:
      - NODE_ENV=production
    command: npm run start

  nginx:
    ports:
      - "80:80"
      - "443:443"
```

Deploy with: `docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d`

## 🔧 Configuration

### Stripe Setup

1. Create Stripe account and get API keys
2. Create products and prices in Stripe Dashboard
3. Setup webhook endpoint: `https://yourdomain.com/api/v1/billing/webhook/stripe/`
4. Add webhook events: `payment_intent.succeeded`, `customer.subscription.updated`

### Email Setup (Resend)

1. Create Resend account
2. Verify your domain
3. Get API key and add to environment

### Google OAuth Setup

1. Go to Google Cloud Console
2. Create OAuth 2.0 client ID
3. Add authorized origins: `https://yourdomain.com`
4. Add redirect URIs: `https://yourdomain.com/api/v1/auth/social/google/`

## 📊 Monitoring and Maintenance

### Logs

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f celery

# Database backup
docker-compose exec db pg_dump -U postgres saas_mvp > backup.sql
```

### Updates

```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose build
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate
```

### Health Checks

- **Application**: `https://yourdomain.com/health`
- **API**: `https://yourdomain.com/api/v1/`
- **Admin**: `https://yourdomain.com/admin/`

## 🔒 Security Considerations

- Use strong SECRET_KEY in production
- Enable HTTPS with valid SSL certificates
- Configure rate limiting in Nginx
- Use environment variables for sensitive data
- Regular security updates
- Enable Stripe webhook signature verification
- Configure CORS properly for your domain

## 📈 Scaling

### Database Scaling
- Enable PostgreSQL connection pooling
- Add read replicas for read-heavy workloads
- Consider PostgreSQL clustering

### Application Scaling
- Increase Docker container replicas
- Use load balancer for multiple servers
- Implement Redis clustering for sessions

### CDN and Static Files
- Use AWS S3 + CloudFront for static files
- Configure Django storages for production

## 🆘 Troubleshooting

### Common Issues

1. **Database connection errors**:
   - Check PostgreSQL service: `docker-compose ps db`
   - Verify environment variables

2. **Celery tasks not running**:
   - Check Redis connection: `docker-compose logs redis`
   - Restart Celery: `docker-compose restart celery`

3. **Frontend build errors**:
   - Clear node_modules: `rm -rf frontend/node_modules`
   - Rebuild: `docker-compose build frontend`

4. **SSL certificate issues**:
   - Verify certificate files exist
   - Check certificate validity: `openssl x509 -in cert.pem -text -noout`

### Support

For issues and questions:
- Check application logs
- Review Django and Nuxt documentation
- Open GitHub issues for bugs

## 📄 License

MIT License - see LICENSE file for details.