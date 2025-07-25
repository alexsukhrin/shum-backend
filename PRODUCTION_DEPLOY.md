# Production Deployment Setup

## 🚀 CI/CD Production Deploy Configuration

This project now includes automated production deployment to EC2 via GitHub Actions when pushing to `main` branch.

## 📋 Required GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions

### Secrets (sensitive data):
```
DJANGO_SECRET_KEY=your-very-long-secret-key-here
DJANGO_ADMIN_URL=your-custom-admin-url/
DATABASE_URL=postgres://user:password@postgres:5432/shum_production
POSTGRES_PASSWORD=your-postgres-password

EMAIL_HOST_PASSWORD=your-email-app-password
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
SENTRY_DSN=your-sentry-dsn
EC2_SSH_KEY=your-ec2-private-key-content
```

### Variables (non-sensitive data):
```
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=shum_production
POSTGRES_USER=postgres
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_USE_TLS=True
DJANGO_AWS_STORAGE_BUCKET_NAME=your-bucket-name
PRODUCTION_HOST=your-ec2-ip-or-domain
EC2_USERNAME=ec2-user
```

## 🖥️ Server Setup (EC2)

### 1. Install Docker on EC2:
```bash
# Update system
sudo yum update -y

# Install Docker
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Log out and log back in for docker group to take effect
exit
# SSH back in
```

### 2. Create required volumes:
```bash
# Create static files volume
docker volume create static_volume
```

## 🔄 Deployment Process

When you push to `main` branch, GitHub CI/CD will:

1. **Run tests** - Linting and pytest
2. **Build Docker image** - With commit SHA tag
3. **Push to GitHub Container Registry**
4. **SSH to EC2 server**
5. **Pull new image**
6. **Stop old container**
7. **Run database migrations** (against AWS RDS)
8. **Create cache table** (for Django database caching)
9. **Collect static files** (to local volume)
10. **Start new Django container** with all environment variables
11. **Clean up old images**

## 🏗️ Architecture

**Services running on EC2:**
- **Django** - Main application (with database caching)

**External AWS services:**
- **RDS PostgreSQL** - Managed database
- **S3** - Static files storage (optional)

## 🔧 Manual Deployment Commands

If you need to deploy manually:

```bash
# On your local machine
docker build -f ./compose/production/django/Dockerfile -t ghcr.io/alexsukhrin/shum-backend:manual .
docker push ghcr.io/alexsukhrin/shum-backend:manual

# On EC2 server - stop old container and start new one
docker stop shum-production-django || true
docker rm shum-production-django || true

docker run -d \
  --name shum-production-django \
  --restart=unless-stopped \
  -p 8032:5000 \
  -v static_volume:/app/staticfiles \
  -e DATABASE_URL="postgres://user:pass@your-rds:5432/db" \
  -e POSTGRES_HOST="your-rds-endpoint" \
  -e POSTGRES_PORT="5432" \
  -e POSTGRES_DB="your-db" \
  -e POSTGRES_USER="your-user" \
  -e POSTGRES_PASSWORD="your-password" \
  -e DJANGO_SETTINGS_MODULE=config.settings.production \
  -e DJANGO_SECRET_KEY="your-secret-key" \
  -e DJANGO_ADMIN_URL="admin/" \
  -e DJANGO_ALLOWED_HOSTS="your-domain.com,your-ip" \
  ghcr.io/alexsukhrin/shum-backend:manual
```

## 🌐 Domain Setup

Don't forget to:
1. Point your domain to EC2 public IP
2. Update `DJANGO_ALLOWED_HOSTS` with your domain
3. Configure SSL certificates (Let's Encrypt via Traefik)

## 📊 Monitoring

- Check logs: `docker logs shum-production-django`
- Container status: `docker ps | grep shum`
- Django admin: `http://your-domain.com:8032/your-admin-url/`

## 🔐 Security Notes

- Use strong passwords for all services
- Enable EC2 security groups properly
- Use IAM roles for AWS services
- Keep secrets in GitHub Secrets, not in code
- Regularly update dependencies and base images
