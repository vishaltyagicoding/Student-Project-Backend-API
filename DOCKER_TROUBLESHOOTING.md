# Docker Troubleshooting Guide

## Issue: ERR_TIMED_OUT when accessing localhost:8000

### Root Cause
Gunicorn workers were hanging during startup, likely due to Celery app initialization in `config/__init__.py` causing blocking behavior.

### Solution
Switch to Django's development server for local development:

```yaml
command: python manage.py runserver 0.0.0.0:8000
```

For production, use Gunicorn with proper configuration.

## Common Issues and Solutions

### 1. Container Won't Start

**Check logs:**
```bash
docker-compose logs web
docker-compose logs celery
```

**Rebuild container:**
```bash
docker-compose down
docker-compose up -d --build
```

### 2. Database Connection Errors

**Ensure environment variables are set correctly:**
- `DB_HOST=postgres` (not localhost)
- `REDIS_HOST=redis` (not localhost)

**Check if PostgreSQL is healthy:**
```bash
docker-compose ps postgres
```

### 3. Port Already in Use

**Find and kill process using port 8000:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9
```

### 4. Static Files Not Loading

**Collect static files:**
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### 5. Celery Tasks Not Running

**Check Celery worker logs:**
```bash
docker-compose logs celery -f
```

**Restart Celery:**
```bash
docker-compose restart celery
```

### 6. Permission Denied Errors

**Fix file permissions:**
```bash
docker-compose exec web chown -R root:root /app
```

### 7. Module Not Found Errors

**Rebuild with no cache:**
```bash
docker-compose build --no-cache
docker-compose up -d
```

## Development vs Production

### Development Setup (Current)
- Uses Django development server
- DEBUG=True
- Hot reload enabled
- Detailed error pages

### Production Setup
- Use Gunicorn with multiple workers
- DEBUG=False
- Static files served by Nginx
- Proper logging configuration

## Switching Between Modes

### For Development (Current Configuration)
```yaml
web:
  command: python manage.py runserver 0.0.0.0:8000
  environment:
    - DEBUG=True
```

### For Production
```yaml
web:
  command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4 --timeout 120
  environment:
    - DEBUG=False
```

## Useful Commands

```bash
# View all container status
docker-compose ps

# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f web

# Execute command in container
docker-compose exec web python manage.py shell

# Restart specific service
docker-compose restart web

# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Rebuild specific service
docker-compose build web

# Scale Celery workers
docker-compose up -d --scale celery=3
```

## Health Checks

### Check if services are responding

**Web service:**
```bash
curl http://localhost:8000
```

**Flower dashboard:**
```bash
curl http://localhost:5555
```

**PostgreSQL:**
```bash
docker-compose exec postgres pg_isready -U postgres
```

**Redis:**
```bash
docker-compose exec redis redis-cli ping
```

## Performance Optimization

### Reduce Build Time
- Use `.dockerignore` to exclude unnecessary files
- Leverage Docker layer caching
- Use multi-stage builds for production

### Reduce Container Size
- Use slim/alpine base images
- Remove unnecessary dependencies
- Clean up apt cache

### Improve Startup Time
- Remove unnecessary migrations
- Optimize database queries
- Use connection pooling

## Security Best Practices

1. Never commit `.env` files with sensitive data
2. Use strong passwords for database
3. Change SECRET_KEY in production
4. Set DEBUG=False in production
5. Configure ALLOWED_HOSTS properly
6. Use HTTPS in production
7. Keep dependencies updated
8. Scan images for vulnerabilities

## Monitoring

### Container Resource Usage
```bash
docker stats
```

### Application Logs
```bash
docker-compose exec web tail -f /app/logs/django.log
```

### Database Logs
```bash
docker-compose logs postgres
```

## Backup and Restore

### Backup Database
```bash
docker-compose exec postgres pg_dump -U postgres student_managements > backup.sql
```

### Restore Database
```bash
docker-compose exec -T postgres psql -U postgres student_managements < backup.sql
```

### Backup Volumes
```bash
docker run --rm -v student_project_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz /data
```

## Getting Help

If you encounter issues not covered here:

1. Check container logs: `docker-compose logs <service>`
2. Verify environment variables in `.env`
3. Ensure all services are healthy: `docker-compose ps`
4. Check Django logs: `/app/logs/django.log`
5. Review Docker documentation: https://docs.docker.com/
6. Review Django documentation: https://docs.djangoproject.com/
