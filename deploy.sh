#!/bin/bash

# Deployment script for Asanbay Website
# Usage: ./deploy.sh

set -e

echo "🚀 Starting deployment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "📝 Creating .env from env.example..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your production settings before continuing!"
    echo "   Important: Set SECRET_KEY, POSTGRES_PASSWORD, and ALLOWED_HOSTS"
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install Docker Compose."
    exit 1
fi

echo "📦 Building and starting containers..."
docker-compose -f docker-compose.yml up -d --build

echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check service health
echo "🔍 Checking service health..."
docker-compose ps

echo "📊 Running database migrations..."
docker-compose exec -T web python manage.py migrate --noinput

echo "📁 Collecting static files..."
docker-compose exec -T web python manage.py collectstatic --noinput

echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Create a superuser: docker-compose exec web python manage.py createsuperuser"
echo "   2. Check logs: docker-compose logs -f"
echo "   3. Visit your site at http://localhost (or your domain)"
echo ""
echo "📚 For more information, see DEPLOYMENT.md"


