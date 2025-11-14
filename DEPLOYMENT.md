# Deployment Guide

This guide explains how to deploy the Asanbay Website to a cloud VM using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- A cloud VM with at least 2GB RAM and 2 CPU cores
- Domain name (optional, for SSL)

## Quick Start

1. **Clone the repository** to your VM:
   ```bash
   git clone <your-repo-url>
   cd "Asanbay Website"
   ```

2. **Create environment file**:
   ```bash
   cp env.example .env
   ```

3. **Edit `.env` file** with your production settings:
   ```bash
   nano .env
   ```
   
   Important settings to change:
   - `SECRET_KEY`: Generate a new secret key (use `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `POSTGRES_PASSWORD`: Use a strong password
   - `ALLOWED_HOSTS`: Add your domain name(s)
   - `DEBUG`: Set to `False` for production

4. **Build and start services**:
   ```bash
   docker-compose -f docker-compose.yml up -d --build
   ```

5. **Create superuser** (optional):
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

6. **Verify deployment**:
   ```bash
   docker-compose ps
   curl http://localhost
   ```

## Services

The deployment includes three services:

- **web**: Django application (Gunicorn WSGI server)
- **db**: PostgreSQL 18 database
- **nginx**: Reverse proxy and static file server

## Configuration

### Environment Variables

All configuration is done through the `.env` file. See `env.example` for available options.

### Nginx Configuration

The nginx configuration is in `nginx/nginx.conf`. For HTTPS:

1. Place your SSL certificates in `nginx/ssl/`:
   - `cert.pem` (certificate)
   - `key.pem` (private key)

2. Uncomment the HTTPS server block in `nginx/nginx.conf`

3. Update the `server_name` directive with your domain

4. Uncomment the HTTP to HTTPS redirect block

### Static and Media Files

- Static files are collected automatically on startup
- Static files are served by nginx from `/app/staticfiles`
- Media files are stored in a Docker volume and served by nginx from `/app/media`

## Maintenance

### View logs:
```bash
docker-compose logs -f
docker-compose logs -f web
docker-compose logs -f nginx
```

### Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

### Collect static files:
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Access Django shell:
```bash
docker-compose exec web python manage.py shell
```

### Backup database:
```bash
docker-compose exec db pg_dump -U asanbay_user asanbay_db > backup.sql
```

### Restore database:
```bash
docker-compose exec -T db psql -U asanbay_user asanbay_db < backup.sql
```

### Update application:
```bash
git pull
docker-compose -f docker-compose.yml up -d --build
```

## Security Considerations

1. **Change default passwords** in `.env`
2. **Use strong SECRET_KEY** (never commit to git)
3. **Set DEBUG=False** in production
4. **Configure ALLOWED_HOSTS** with your domain
5. **Enable HTTPS** with SSL certificates
6. **Keep dependencies updated**: `docker-compose pull && docker-compose up -d --build`
7. **Use firewall** to restrict access to ports 80/443 only

## Troubleshooting

### Database connection errors:
- Check if database container is healthy: `docker-compose ps`
- Verify environment variables in `.env`
- Check database logs: `docker-compose logs db`

### Static files not loading:
- Run collectstatic: `docker-compose exec web python manage.py collectstatic --noinput`
- Check nginx logs: `docker-compose logs nginx`
- Verify volume mounts: `docker-compose exec nginx ls -la /app/staticfiles`

### Application errors:
- Check application logs: `docker-compose logs web`
- Verify environment variables
- Check Django settings

## Scaling

To scale the web service:
```bash
docker-compose up -d --scale web=3
```

Note: You may need to adjust nginx upstream configuration for load balancing.

## Monitoring

Health checks are configured for all services. Monitor with:
```bash
docker-compose ps
```

All services should show as "healthy" when running correctly.


