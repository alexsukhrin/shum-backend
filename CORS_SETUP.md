# CORS Configuration Guide

## Overview

Cross-Origin Resource Sharing (CORS) дозволяє вашому frontend додатку робити запити до API на різних доменах.

**⚡ MVP Status:** Наразі проект налаштований для швидкого deployment з `CORS_ALLOW_ALL_ORIGINS = True` і в development, і в production для максимальної гнучкості під час розробки MVP.

## Development (Local)

### Current Configuration
```python
# config/settings/local.py
CORS_ALLOW_ALL_ORIGINS = True  # ⚠️ ONLY for development!
CORS_ALLOW_CREDENTIALS = True
```

### Alternative Development Setup
Якщо ви хочете більше контролю в розробці:

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
Наразі production використовує відкриті CORS налаштування для швидкого deployment:

```python
# config/settings/production.py
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=True)  # ⚡ MVP
```

### Transition to Secure Configuration (After MVP)
Коли будете готові до production security, перейдіть на обмежений список доменів:

```python
# config/settings/production.py
CORS_ALLOW_ALL_ORIGINS = False  # ✅ Secure
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[...])
```

### MVP to Production Security Transition

**Коли переходити на безпечні налаштування:**
- ✅ MVP завершено і працює стабільно
- ✅ Є фіксованi production домени
- ✅ Frontend готовий до deployment
- ✅ Немає потреби в частих змінах доменів

**Як зробити перехід:**

1. **Встановіть environment variable:**
```bash
# У вашому .env.production файлі
CORS_ALLOW_ALL_ORIGINS=False
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://app.yourdomain.com
```

2. **Код вже готовий в production.py** - налаштування автоматично застосуються

3. **Протестуйте з реальними доменами**

### Example Use Cases

#### SPA (Single Page Application)
```bash
# React/Vue/Angular app
CORS_ALLOWED_ORIGINS=https://app.yourdomain.com,https://yourdomain.com
```

#### Mobile App with WebView
```bash
# Додайте file:// для локальних файлів в мобільних додатках
CORS_ALLOWED_ORIGINS=https://yourdomain.com,file://,capacitor://localhost
```

#### Multiple Environments
```bash
# Production + Staging
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://staging.yourdomain.com,https://dev.yourdomain.com
```

#### Subdomain Support
```bash
# Головний домен та поддомени
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com,https://admin.yourdomain.com
```

## API Endpoints

Переконайтесь що ваш frontend використовує правильні URL:

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
**Причина:** Ваш домен не в `CORS_ALLOWED_ORIGINS`
**Рішення:** Додайте ваш домен до environment variable

#### "CORS policy: credentials mode"
**Причина:** `CORS_ALLOW_CREDENTIALS = False`
**Рішення:** Встановіть `CORS_ALLOW_CREDENTIALS = True`

#### "Method not allowed"
**Причина:** HTTP метод не в `CORS_ALLOWED_METHODS`
**Рішення:** Перевірте що використовуєте POST/GET/PUT/DELETE

### Security Warnings

❌ **НІКОЛИ не використовуйте в production:**
```python
CORS_ALLOW_ALL_ORIGINS = True  # Небезпечно!
```

✅ **Завжди використовуйте конкретні домени:**
```python
CORS_ALLOWED_ORIGINS = ["https://yourdomain.com"]
```

## Production Deployment Checklist

### MVP Phase (Current)
- [x] CORS налаштовано для максимальної гнучкості (`CORS_ALLOW_ALL_ORIGINS = True`)
- [ ] Тестування з різних доменів/frontend додатків
- [ ] Моніторинг безпеки та зловживань

### Production Security Phase (Future)
- [ ] Встановлено `CORS_ALLOW_ALL_ORIGINS = False`
- [ ] Додано тільки необхідні домени в `CORS_ALLOWED_ORIGINS`
- [ ] Перевірено що HTTPS використовується (не HTTP)
- [ ] Протестовано CORS з production доменами
- [ ] Видалено тестові/development домени
- [ ] Налаштовано monitoring для CORS помилок

## Need Help?

Якщо у вас проблеми з CORS:
1. Перевірте Network tab в Developer Tools браузера
2. Подивіться на preflight OPTIONS requests
3. Переконайтеся що response headers містять `Access-Control-Allow-Origin`
4. Перевірте що ваш домен точно співпадає з тим що в `CORS_ALLOWED_ORIGINS`
