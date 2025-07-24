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
REDIS_URL=redis://redis:6379/0
EMAIL_HOST_PASSWORD=your-email-app-password
DJANGO_AWS_ACCESS_KEY_ID=your-aws-access-key
DJANGO_AWS_SECRET_ACCESS_KEY=your-aws-secret-key
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

### 1. Install Docker and Docker Compose on EC2:
```bash
# Update system
sudo yum update -y

# Install Docker
sudo yum install -y docker
sudo service docker start
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### 2. Create required directories:
```bash
# Create project directory
mkdir -p /home/ec2-user/shum
cd /home/ec2-user/shum

# No .env file needed - all variables come from GitLab CI/CD
```

### 3. Create Docker network and volumes:
```bash
# Create network
docker network create shum-production-net

# Create volumes
docker volume create static_volume
```

## 🔄 Deployment Process

When you push to `main` branch, GitLab CI/CD will:

1. **Run tests** - Linting and pytest
2. **Build Docker image** - With commit SHA tag
3. **Push to GitHub Container Registry**
4. **SSH to EC2 server**
5. **Pull new image**
6. **Stop old containers**
7. **Run database migrations** (against AWS RDS)
8. **Collect static files** (to AWS S3 or local volume)
9. **Start new containers** with all environment variables from GitLab
10. **Clean up old images**

## 🏗️ Architecture

**Services running on EC2:**
- **Django** - Main application
- **Redis** - Caching and sessions
- **Traefik** - Reverse proxy and SSL

**External AWS services:**
- **RDS PostgreSQL** - Managed database
- **S3** - Static files storage (optional)

## 🔧 Manual Deployment Commands

If you need to deploy manually:

```bash
# On your local machine
docker build -f ./compose/production/django/Dockerfile -t ghcr.io/alexsukhrin/shum-backend:manual .
docker push ghcr.io/alexsukhrin/shum-backend:manual

# On EC2 server (set all environment variables)
export DJANGO_IMAGE=ghcr.io/alexsukhrin/shum-backend:manual
export DATABASE_URL="postgres://marketplace_user:marketplace_password@postgres-instance.cby2c0iga8z1.eu-central-1.rds.amazonaws.com:5432/marketplace?sslmode=require"
export DJANGO_SECRET_KEY="your-secret-key"
# ... set all other variables ...
docker-compose -f docker-compose.production.yml up -d
```

## 🌐 Domain Setup

Don't forget to:
1. Point your domain to EC2 public IP
2. Update `DJANGO_ALLOWED_HOSTS` with your domain
3. Configure SSL certificates (Let's Encrypt via Traefik)

## 📊 Monitoring

- Check logs: `docker-compose -f docker-compose.production.yml logs`
- Container status: `docker-compose -f docker-compose.production.yml ps`
- Django admin: `https://your-domain.com/your-admin-url/`

## 🔐 Security Notes

- Use strong passwords for all services
- Enable EC2 security groups properly
- Use IAM roles for AWS services
- Keep secrets in GitHub Secrets, not in code
- Regularly update dependencies and base images
