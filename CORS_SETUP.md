# CORS Configuration Guide

## Overview

Cross-Origin Resource Sharing (CORS) allows your frontend application to make requests to the API on different domains.

**⚡ MVP Status:** Currently, the project is configured for quick deployment with `CORS_ALLOW_ALL_ORIGINS = True` in both development and production for maximum flexibility during MVP development.

## Development (Local)

### Current Configuration
```python
# config/settings/local.py
CORS_ALLOW_ALL_ORIGINS = True  # ⚠️ ONLY for development!
CORS_ALLOW_CREDENTIALS = True
```

### Alternative Development Setup
If you want more control in development:

```python
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",    # React dev server
    "http://127.0.0.1:3000",
    "http://localhost:8080",    # Vue dev server
    "http://127.0.0.1:8080",
    "http://localhost:4200",    # Angular dev server
    "http://127.0.0.1:4200",
]
```

## Production

### Current MVP Configuration
Currently, production uses open CORS settings for quick deployment:

```python
# config/settings/production.py
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=True)  # ⚡ MVP
```

### Transition to Secure Configuration (After MVP)
When you're ready for production security, switch to a restricted list of domains:

```python
# config/settings/production.py
CORS_ALLOW_ALL_ORIGINS = False  # ✅ Secure
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[...])
```

### MVP to Production Security Transition

**When to switch to secure settings:**
- ✅ MVP is complete and working stably
- ✅ You have fixed production domains
- ✅ Frontend is ready for deployment
- ✅ No need for frequent domain changes

**How to make the transition:**

1. **Set environment variable:**
```bash
# In your .env.production file
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://app.yourdomain.com
```

2. **Code is already ready in production.py** - settings will be applied automatically

3. **Test with real domains**

### Example Use Cases

#### SPA (Single Page Application)
```bash
# React/Vue/Angular app
CORS_ALLOWED_ORIGINS=https://app.yourdomain.com,https://yourdomain.com
```

#### Mobile App with WebView
```bash
# Add file:// for local files in mobile apps
CORS_ALLOWED_ORIGINS=https://yourdomain.com,file://,capacitor://localhost
```

#### Multiple Environments
```bash
# Production + Staging
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://staging.yourdomain.com,https://dev.yourdomain.com
```

#### Subdomain Support
```bash
# Main domain and subdomains
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com,https://admin.yourdomain.com
```

## API Endpoints

Make sure your frontend uses the correct URLs:

### Authentication
- ✅ `POST /api/auth/register/`
- ✅ `POST /api/auth/login/`
- ✅ `GET /api/auth/profile/`

### Resources
- ✅ `GET /api/users/`
- ✅ `GET /api/ads/`
- ✅ `GET /api/docs/` (API Documentation)

## Testing CORS

### Command Line Test
```bash
curl -H "Origin: https://yourdomain.com" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     http://localhost:8000/api/auth/register/
```

### Browser Console Test
```javascript
fetch('http://localhost:8000/api/auth/register/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        email: 'test@example.com',
        first_name: 'Test',
        last_name: 'User',
        password: 'testpassword123'
    })
})
.then(response => console.log('Success:', response))
.catch(error => console.error('CORS Error:', error));
```

## Troubleshooting

### Common CORS Errors

#### "Access-Control-Allow-Origin missing"
**Cause:** Your domain is not in `CORS_ALLOWED_ORIGINS`
**Solution:** Add your domain to the environment variable

#### "CORS policy: credentials mode"
**Cause:** `CORS_ALLOW_CREDENTIALS = False`
**Solution:** Set `CORS_ALLOW_CREDENTIALS = True`

#### "Method not allowed"
**Cause:** HTTP method is not in `CORS_ALLOWED_METHODS`
**Solution:** Check that you're using POST/GET/PUT/DELETE

### Security Warnings

❌ **NEVER use in production:**
```python
CORS_ALLOW_ALL_ORIGINS = True  # Dangerous!
```

✅ **Always use specific domains:**
```python
CORS_ALLOWED_ORIGINS = ["https://yourdomain.com"]
```

## Production Deployment Checklist

### MVP Phase (Current)
- [x] CORS configured for maximum flexibility (`CORS_ALLOW_ALL_ORIGINS = True`)
- [ ] Testing with different domains/frontend applications
- [ ] Security and abuse monitoring

### Production Security Phase (Future)
- [ ] Set `CORS_ALLOW_ALL_ORIGINS = False`
- [ ] Add only necessary domains to `CORS_ALLOWED_ORIGINS`
- [ ] Verify that HTTPS is used (not HTTP)
- [ ] Test CORS with production domains
- [ ] Remove test/development domains
- [ ] Set up monitoring for CORS errors

## Need Help?

If you have CORS issues:
1. Check the Network tab in browser Developer Tools
2. Look at preflight OPTIONS requests
3. Make sure response headers contain `Access-Control-Allow-Origin`
4. Verify that your domain exactly matches what's in `CORS_ALLOWED_ORIGINS`
