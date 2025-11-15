# Deployment Guide

This guide explains how to deploy the Asanbay Website to a cloud VM using Docker and Docker Compose.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- A cloud VM with at least 2GB RAM and 2 CPU cores
- Domain name configured: `asanbay.org` (already set in configuration)

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
   - `ALLOWED_HOSTS`: Already configured for `asanbay.org` and `www.asanbay.org` (can be modified if needed)
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

## Deployment with Dokploy

If you're deploying using Dokploy on your internal server, use the `docker-compose.dokploy.yml` file instead of `docker-compose.yml`.

### Key Differences for Dokploy:

1. **Nginx + Traefik**: Nginx handles static files and reverse proxies to Django, while Traefik handles SSL and domain routing
2. **Traefik Labels**: The nginx service includes Traefik labels for automatic SSL and domain routing
3. **External Network**: Uses `dokploy-network` (external network managed by Dokploy)
4. **Automatic SSL**: Traefik automatically handles SSL certificates via Let's Encrypt
5. **No Port Mapping**: Nginx doesn't expose ports directly - Traefik routes traffic to nginx on port 80

### Steps to Deploy with Dokploy:

1. **In Dokploy Dashboard**:
   - Navigate to "Compose" section
   - Create a new Compose service
   - Set the compose file path to `docker-compose.dokploy.yml`

2. **Configure Environment Variables**:
   - Set all required environment variables in Dokploy's environment section
   - Ensure `ALLOWED_HOSTS` includes `asanbay.org` and `www.asanbay.org`
   - Set `DEBUG=False` for production
   - Configure `SECRET_KEY` and database credentials

3. **Domain Configuration**:
   - The Traefik labels are already configured for `asanbay.org` and `www.asanbay.org`
   - SSL certificates will be automatically provisioned by Let's Encrypt
   - The configuration includes automatic www to non-www redirect

4. **Deploy**:
   - Dokploy will handle the build and deployment process
   - Monitor the deployment logs in the Dokploy dashboard

### Static Files with Dokploy:

Nginx handles static and media files efficiently, serving them directly without hitting Django. The `collectstatic` command runs automatically on container startup, and nginx serves the collected static files from the shared volume.

## Services

### Standard Deployment (docker-compose.yml):
- **web**: Django application (Gunicorn WSGI server)
- **db**: PostgreSQL 18 database
- **nginx**: Reverse proxy and static file server

### Dokploy Deployment (docker-compose.dokploy.yml):
- **web**: Django application (Gunicorn WSGI server)
- **db**: PostgreSQL 18 database
- **nginx**: Reverse proxy and static file server - exposed via Traefik

## Configuration

### Environment Variables

All configuration is done through the `.env` file. See `env.example` for available options.

### Nginx Configuration

The nginx configuration is in `nginx/nginx.conf`. For HTTPS:

1. Place your SSL certificates in `nginx/ssl/`:
   - `cert.pem` (certificate)
   - `key.pem` (private key)

2. Uncomment the HTTPS server block in `nginx/nginx.conf` (already configured for `asanbay.org` and `www.asanbay.org`)

3. The `server_name` directive is already set to `asanbay.org` and `www.asanbay.org`

4. Uncomment the HTTP to HTTPS redirect block (already configured for `asanbay.org`)

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
4. **ALLOWED_HOSTS** is already configured for `asanbay.org` and `www.asanbay.org`
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



