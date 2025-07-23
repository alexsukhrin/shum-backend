# S3 Storage for Marketplace Images

## 🎯 **Статус S3 Storage:**

### **✅ В Production (AWS EC2):**
```python
# Картинки загружаются в S3
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": "marketplace-bucket-nwnu4de2",
            "location": "media",
            "default_acl": "public-read",
        },
    },
}
MEDIA_URL = "https://marketplace-bucket-nwnu4de2.s3.amazonaws.com/media/"
```

### **🏠 В Development (локально):**
```python
# Картинки сохраняются локально для тестирования
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage"
    },
}
MEDIA_URL = "/media/"
```

## 📦 **AWS S3 Configuration**

Your marketplace project is configured to store all media files (photos, avatars) in AWS S3 while keeping static files local for Traefik to serve.

### **🎯 What's stored in S3:**
- ✅ **User avatars** (`avatars/user_{id}/filename.jpg`)
- ✅ **Product images** (`products/product_{id}/filename.jpg`)
- ✅ **Any uploaded media files**

### **🏠 What's stored locally:**
- ✅ **Static files** (CSS, JS, admin assets) served by Traefik
- ✅ **Django admin media**

## 🔧 **Current Configuration**

### **S3 Settings (Production):**
```python
# AWS S3 Configuration
AWS_STORAGE_BUCKET_NAME = "your-marketplace-bucket"
AWS_S3_REGION_NAME = "eu-central-1"
AWS_S3_CUSTOM_DOMAIN = "your-marketplace-bucket.s3.amazonaws.com"
MEDIA_URL = "https://your-marketplace-bucket.s3.amazonaws.com/media/"

# Storage backend for media files
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "bucket_name": "your-marketplace-bucket",
            "region_name": "eu-central-1",
            "location": "media",
            "file_overwrite": False,
            "default_acl": "public-read",
        },
    },
}
```

### **Required AWS Variables:**
```env
DJANGO_AWS_ACCESS_KEY_ID=your-access-key-here
DJANGO_AWS_SECRET_ACCESS_KEY=your-secret-access-key-here
DJANGO_AWS_STORAGE_BUCKET_NAME=your-bucket-name-here
AWS_DEFAULT_REGION=eu-central-1
```

## 🚀 **API Endpoints for Images**

### **User Avatar Upload:**
**PATCH** `/api/users/{id}/` (with `avatar` field)
```bash
curl -X PATCH http://localhost:8000/api/users/1/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "avatar=@profile_picture.jpg"
```

### **Ad Creation:**
**POST** `/api/ads/`
```json
{
  "title": "iPhone 15 Pro for Sale",
  "description": "Excellent condition, used for 6 months",
  "price": "850.00",
  "is_active": true
}
```

### **Ad Image Upload:**
**POST** `/api/ads/{id}/upload_image/`
```bash
curl -X POST http://localhost:8000/api/ads/1/upload_image/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "image=@phone_photo.jpg" \
  -F "alt_text=iPhone front view" \
  -F "order=1"
```

### **Mark Ad as Sold:**
**POST** `/api/ads/{id}/mark_sold/`
```bash
curl -X POST http://localhost:8000/api/ads/1/mark_sold/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📱 **Example API Responses**

### **User with Avatar:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "name": "John Doe",
  "avatar": "avatars/user_1/profile.jpg",
  "avatar_url": "https://your-bucket.s3.amazonaws.com/media/avatars/user_1/profile.jpg"
}
```

### **Ad with Images:**
```json
{
  "id": 1,
  "title": "iPhone 15 Pro for Sale",
  "description": "Excellent condition, used for 6 months",
  "price": "850.00",
  "is_active": true,
  "is_sold": false,
  "owner": 1,
  "owner_info": {
    "id": 1,
    "email": "seller@example.com",
    "name": "John Seller"
  },
  "main_image_url": "https://your-bucket.s3.amazonaws.com/media/ads/ad_1/main.jpg",
  "images": [
    {
      "id": 1,
      "image": "ads/ad_1/main.jpg",
      "image_url": "https://your-bucket.s3.amazonaws.com/media/ads/ad_1/main.jpg",
      "alt_text": "iPhone front view",
      "order": 1,
      "created_at": "2025-01-22T10:30:00Z"
    }
  ],
  "created_at": "2025-01-22T10:00:00Z",
  "updated_at": "2025-01-22T10:30:00Z"
}
```

## 🏗️ **File Structure in S3**

```
your-marketplace-bucket/
├── media/
│   ├── avatars/
│   │   ├── user_1/
│   │   │   ├── profile.jpg
│   │   │   └── avatar_2025.png
│   │   └── user_2/
│   │       └── selfie.jpg
│   └── ads/
│       ├── ad_1/
│       │   ├── main.jpg
│       │   ├── side_view.jpg
│       │   └── back_view.jpg
│       └── ad_2/
│           └── photo.png
```

## 🔒 **S3 Bucket Configuration**

### **Required Bucket Policy:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::your-marketplace-bucket/media/*"
    }
  ]
}
```

### **CORS Configuration:**
```json
[
  {
    "AllowedHeaders": ["*"],
    "AllowedMethods": ["GET", "POST", "PUT", "DELETE"],
    "AllowedOrigins": ["*"],
    "ExposeHeaders": ["ETag"]
  }
]
```

## 🧪 **Testing S3 Storage**

### **1. Development (Локально):**
⚠️ **ВАЖНО: Никогда не коммитите реальные AWS ключи в Git!**

Для локального тестирования можно настроить S3, добавив AWS credentials:

```env
# .envs/.local/.django
DJANGO_AWS_ACCESS_KEY_ID=
DJANGO_AWS_SECRET_ACCESS_KEY=
DJANGO_AWS_STORAGE_BUCKET_NAME=
AWS_DEFAULT_REGION=eu-central-1
```

### **2. Production проверка:**
```bash
# 1. Загрузить картинку через API
curl -X POST http://your-domain.com/api/ads/1/upload_image/ \
  -H "Authorization: Bearer TOKEN" \
  -F "image=@test_image.jpg"

# 2. Проверить что URL ведет на S3
curl -I "https://your-bucket.s3.amazonaws.com/media/ads/ad_1/image.jpg"
```

### **3. Проверка настроек в Django shell:**
```python
# На production сервере
python manage.py shell

>>> from django.conf import settings
>>> print(settings.STORAGES['default']['BACKEND'])
# Должно быть: 'storages.backends.s3.S3Storage'

>>> print(settings.MEDIA_URL)
# Должно быть: 'https://your-bucket.s3.amazonaws.com/media/'
```

## 🚨 **Important Notes**

### **File Overwrite Protection:**
- `AWS_S3_FILE_OVERWRITE = False` - files with same name get unique suffixes
- Example: `image.jpg` → `image_AbCdEf.jpg`

### **Public Access:**
- All uploaded images are **public-read** by default
- Perfect for marketplace where product images need to be publicly accessible

### **Cache Control:**
- Images have `max-age=86400` (24 hours) caching
- Improves performance for frequently accessed images

### **Cost Optimization:**
- Only media files go to S3 (images, documents)
- Static files served locally by Traefik (free)
- No unnecessary S3 requests for CSS/JS files

## 📊 **Benefits for Marketplace:**

✅ **Scalability** - S3 handles unlimited image storage
✅ **Performance** - CDN-like delivery from AWS
✅ **Reliability** - 99.999999999% durability
✅ **Cost-effective** - Pay only for storage used
✅ **Global accessibility** - Images accessible worldwide
✅ **Integration** - Seamless with Django models

## 🔧 **Troubleshooting**

### **Images not appearing:**
1. Check AWS credentials in environment variables
2. Verify S3 bucket permissions and CORS
3. Check that `MEDIA_URL` points to correct S3 domain

### **Upload failures:**
1. Verify IAM user has `s3:PutObject` permission
2. Check bucket exists and is in correct region
3. Ensure file size doesn't exceed limits

**Your marketplace is ready for production-scale image storage! 📸**
