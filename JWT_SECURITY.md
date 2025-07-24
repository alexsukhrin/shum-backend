# JWT Security Configuration

## ⚠️ Critical Security Requirements

### 1. DJANGO_SECRET_KEY Environment Variable

**REQUIRED for production!** The JWT tokens are signed using `DJANGO_SECRET_KEY`.

#### ❌ Security Issues Fixed:
- Removed insecure default `"django-insecure-change-me"`
- Added validation to prevent weak keys in production
- Enforced minimum key length (50+ characters)

#### ✅ Production Setup:

1. **Generate a strong secret key:**
```bash
# Method 1: Using Django
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Method 2: Using OpenSSL
openssl rand -base64 64

# Method 3: Using Python
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

2. **Set environment variable:**
```bash
# In production environment
export DJANGO_SECRET_KEY="your-super-long-random-key-here-at-least-50-characters"
```

3. **Docker/Docker Compose:**
```yaml
# docker-compose.production.yml
environment:
  - DJANGO_SECRET_KEY=your-super-long-random-key-here-at-least-50-characters
```

4. **CI/CD Environment:**
```bash
# GitHub Actions
DJANGO_SECRET_KEY: ${{ secrets.DJANGO_SECRET_KEY }}

# AWS/Heroku/etc
# Set as encrypted environment variable in your deployment platform
```

### 2. Security Validation

The application now includes automatic validation:

- ✅ **Development**: Warning if using insecure key
- ❌ **Production**: Application fails to start with insecure key
- ✅ **Minimum length**: Enforces 50+ character keys
- ❌ **Prevents**: Any keys starting with "django-insecure-"

### 3. JWT Configuration

```python
SIMPLE_JWT = {
    "ALGORITHM": "HS256",
    "SIGNING_KEY": env("DJANGO_SECRET_KEY"),  # No default - MUST be set!
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}
```

### 4. Best Practices

#### ✅ Do:
- Use different SECRET_KEY for each environment
- Store SECRET_KEY securely (encrypted environment variables)
- Use minimum 50 character random keys
- Rotate keys periodically
- Monitor for key exposure in logs/code

#### ❌ Don't:
- Commit SECRET_KEY to version control
- Use predictable or short keys
- Share keys between environments
- Log the SECRET_KEY value
- Use the same key for multiple applications

### 5. Key Rotation

If you need to rotate the SECRET_KEY:

1. **Generate new key**
2. **Update environment variable**
3. **Restart application**
4. **All existing JWT tokens become invalid** (users need to re-login)

### 6. Troubleshooting

#### Error: "DJANGO_SECRET_KEY environment variable is required"
- Set the environment variable before starting the application
- Check your environment configuration

#### Error: "DJANGO_SECRET_KEY is insecure for production"
- Generate a new, strong secret key
- Ensure key is 50+ characters
- Remove any "django-insecure-" prefix

#### Warning in development:
- Normal for development with default keys
- Ensure production environment uses secure key

### 7. Security Checklist

Before deploying to production:

- [ ] `DJANGO_SECRET_KEY` environment variable set
- [ ] Secret key is 50+ characters
- [ ] Secret key is random and unique
- [ ] No insecure default keys used
- [ ] Environment variables encrypted/secured
- [ ] Different keys for different environments
- [ ] Application starts without security warnings

## Related Security

See also:
- [AWS Security Configuration](./AWS_SECURITY.md)
- [S3 Storage Security](./S3_STORAGE.md)
- Django Security Settings in `config/settings/production.py`
