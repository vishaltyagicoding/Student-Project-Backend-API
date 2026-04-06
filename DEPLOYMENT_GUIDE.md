# Docker Deployment Guide

This guide explains how to deploy the Student Management System using Docker and Docker Compose.

## Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 2.0 or higher)
- Git

## Project Structure

```
.
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── entrypoint.sh
│   ├── requirements.txt
│   ├── .env
│   └── ... (Django project files)
└── docker-compose.yml
```

## Services Overview

The deployment includes the following services:

1. **postgres** - PostgreSQL 15 database
2. **redis** - Redis cache and message broker
3. **web** - Django application (Gunicorn)
4. **celery** - Celery worker for async tasks
5. **celery-beat** - Celery scheduler for periodic tasks
6. **flower** - Celery monitoring dashboard

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <project-directory>
```

### 2. Configure Environment Variables

Edit `backend/.env` file with your production settings:

```env
# Security
SECRET_KEY=your-super-secret-key-change-this
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DB_NAME=student_managements
DB_USER=postgres
DB_PASSWORD=strong-password-here
DB_HOST=postgres
DB_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=0

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440
```

### 3. Build and Start Services

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Initialize Database

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files (already done in entrypoint)
docker-compose exec web python manage.py collectstatic --noinput
```

## Service Access

- **Django Application**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
- **Flower Dashboard**: http://localhost:5555
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Docker Commands

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### Stop and Remove Volumes
```bash
docker-compose down -v
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f celery
```

### Restart a Service
```bash
docker-compose restart web
docker-compose restart celery
```

### Execute Commands in Container
```bash
# Django shell
docker-compose exec web python manage.py shell

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run migrations
docker-compose exec web python manage.py migrate
```

### Rebuild Services
```bash
# Rebuild all
docker-compose build

# Rebuild specific service
docker-compose build web

# Rebuild and restart
docker-compose up -d --build
```

## Production Deployment

### 1. Security Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `DEBUG=False`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Use strong database passwords
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up firewall rules
- [ ] Enable security headers

### 2. Use Production-Ready Settings

Update `docker-compose.yml` for production:

```yaml
services:
  web:
    environment:
      - DEBUG=False
    # Remove volume mount for code
    # volumes:
    #   - ./backend:/app
```

### 3. Add Nginx Reverse Proxy

Create `nginx/nginx.conf`:

```nginx
upstream django {
    server web:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }
}
```

Add to `docker-compose.yml`:

```yaml
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - web
    networks:
      - app_network
```

### 4. Database Backups

```bash
# Backup
docker-compose exec postgres pg_dump -U postgres student_managements > backup.sql

# Restore
docker-compose exec -T postgres psql -U postgres student_managements < backup.sql
```

## Monitoring

### Flower Dashboard

Access Celery task monitoring at http://localhost:5555

### Container Health

```bash
# Check container status
docker-compose ps

# Check resource usage
docker stats
```

### Application Logs

```bash
# View Django logs
docker-compose exec web tail -f /app/logs/django.log

# View all logs
docker-compose logs -f --tail=100
```

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs service-name

# Rebuild
docker-compose build --no-cache service-name
docker-compose up -d service-name
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Test connection
docker-compose exec web python manage.py dbshell
```

### Celery Tasks Not Running

```bash
# Check Celery worker
docker-compose logs celery

# Restart Celery
docker-compose restart celery
```

### Permission Issues

```bash
# Fix permissions
docker-compose exec web chown -R root:root /app
```

## Scaling

Scale Celery workers:

```bash
docker-compose up -d --scale celery=3
```

## Environment-Specific Configurations

### Development
```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
```

### Production
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Maintenance

### Update Application

```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose up -d --build

# Run migrations
docker-compose exec web python manage.py migrate
```

### Clean Up

```bash
# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove everything
docker system prune -a --volumes
```

## Support

For issues or questions, please refer to:
- Application logs: `/app/logs/django.log`
- Container logs: `docker-compose logs`
- Django documentation: https://docs.djangoproject.com/
- Docker documentation: https://docs.docker.com/
