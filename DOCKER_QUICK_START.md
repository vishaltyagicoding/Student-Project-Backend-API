# Docker Quick Start Guide

## Prerequisites
- Docker Desktop installed and running
- Git (optional)

## Quick Start (Development)

### 1. Start All Services
```bash
docker-compose up -d
```

### 2. Check Status
```bash
docker-compose ps
```

All services should show "Up" status.

### 3. Access the Application

- **Django Application**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api/docs/
- **Flower (Celery Monitor)**: http://localhost:5555

### 4. Create Superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 5. View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
```

## Common Commands

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### Restart a Service
```bash
docker-compose restart web
```

### View Logs
```bash
docker-compose logs -f web
```

### Execute Django Commands
```bash
# Django shell
docker-compose exec web python manage.py shell

# Create migrations
docker-compose exec web python manage.py makemigrations

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic
```

### Rebuild After Code Changes
```bash
docker-compose up -d --build
```

## Production Deployment

### 1. Update Environment Variables
Edit `backend/.env`:
```env
DEBUG=False
SECRET_KEY=your-super-secret-production-key
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DB_PASSWORD=strong-production-password
```

### 2. Start with Production Configuration
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

### 3. Access via Nginx
- **HTTP**: http://your-domain.com
- **HTTPS**: https://your-domain.com (after SSL configuration)

## Troubleshooting

### Can't Access localhost:8000?

1. **Check if containers are running:**
   ```bash
   docker-compose ps
   ```

2. **Check logs for errors:**
   ```bash
   docker-compose logs web
   ```

3. **Restart the web service:**
   ```bash
   docker-compose restart web
   ```

4. **Rebuild if needed:**
   ```bash
   docker-compose up -d --build web
   ```

### Database Connection Issues?

Ensure environment variables are correct:
- `DB_HOST=postgres` (not localhost)
- `REDIS_HOST=redis` (not localhost)

### Port Already in Use?

Stop the conflicting service or change the port in `docker-compose.yml`:
```yaml
ports:
  - "8001:8000"  # Use port 8001 instead
```

## Service Ports

- **Web (Django)**: 8000
- **PostgreSQL**: 5432
- **Redis**: 6379
- **Flower**: 5555
- **Nginx** (production): 80, 443

## Data Persistence

Data is stored in Docker volumes:
- `postgres_data` - Database data
- `redis_data` - Redis data
- `static_volume` - Static files
- `media_volume` - Uploaded media
- `logs_volume` - Application logs

To remove all data:
```bash
docker-compose down -v
```

## Development Workflow

1. Make code changes in your editor
2. Changes are automatically reflected (volume mount)
3. For dependency changes, rebuild:
   ```bash
   docker-compose up -d --build
   ```

## Useful Tips

- Use `docker-compose logs -f` to monitor all services
- Use `docker-compose exec web python manage.py shell` for Django shell
- Use `docker-compose restart <service>` to restart a specific service
- Use `docker-compose down && docker-compose up -d` for a fresh start

## Getting Help

- Check `DOCKER_TROUBLESHOOTING.md` for common issues
- Check `DEPLOYMENT_GUIDE.md` for detailed deployment instructions
- View logs: `docker-compose logs <service>`
- Check container status: `docker-compose ps`

## Next Steps

1. Create a superuser account
2. Access the admin panel
3. Test the API endpoints
4. Monitor Celery tasks in Flower
5. Review the API documentation

Enjoy your Dockerized Django application! 🚀
