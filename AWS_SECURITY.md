# 🔒 AWS Security Guidelines

## ⚠️ **КРИТИЧЕСКИ ВАЖНО: Безопасность AWS ключей**

### **❌ НИКОГДА НЕ ДЕЛАЙТЕ:**

1. **Не коммитите AWS ключи в Git:**
   ```bash
   # ❌ ПЛОХО - любые ключи в коде
   AWS_ACCESS_KEY = ""
   AWS_SECRET_KEY = ""
   ```

2. **Не сохраняйте в публичных файлах:**
   - README.md
   - config файлы в Git
   - Комментарии в коде
   - Документация

3. **Не шарьте в чатах/слаке:**
   - Скриншоты с ключами
   - Копирование .env файлов
   - Логи с credentials

### **✅ ПРАВИЛЬНОЕ ХРАНЕНИЕ:**

#### **1. Локальная разработка:**
```env
# .envs/.local/.django (НЕ в Git!)
DJANGO_AWS_ACCESS_KEY_ID=
DJANGO_AWS_SECRET_ACCESS_KEY=
DJANGO_AWS_STORAGE_BUCKET_NAME=
```

#### **2. Production (GitLab CI/CD):**
```bash
# GitLab → Settings → CI/CD → Variables
DJANGO_AWS_ACCESS_KEY_ID = "secret, masked"
DJANGO_AWS_SECRET_ACCESS_KEY = "secret, masked"
DJANGO_AWS_STORAGE_BUCKET_NAME = "variable"
```

#### **3. Production (GitHub Actions):**
```bash
# GitHub → Settings → Secrets and variables
DJANGO_AWS_ACCESS_KEY_ID = "secret"
DJANGO_AWS_SECRET_ACCESS_KEY = "secret"
```

#### **4. Production Server:**
```bash
# Environment variables
export DJANGO_AWS_ACCESS_KEY_ID=""
export DJANGO_AWS_SECRET_ACCESS_KEY=""

# Or use AWS IAM Role (лучший вариант)
```

### **🛡️ BEST PRACTICES:**

#### **1. Используйте IAM Roles (рекомендуется):**
```bash
# На EC2 instance назначьте IAM Role вместо ключей
# Тогда AWS SDK автоматически получит credentials
```

#### **2. Ограниченные права:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::your-bucket/media/*"
    }
  ]
}
```

#### **3. Ротация ключей:**
- Меняйте ключи каждые 90 дней
- Используйте временные ключи где возможно
- Удаляйте неиспользуемые ключи

#### **4. Мониторинг:**
- Включите CloudTrail для логирования
- Настройте алерты на подозрительную активность
- Проверяйте Access Logs регулярно

### **🚨 ЧТО ДЕЛАТЬ ЕСЛИ КЛЮЧИ СКОМПРОМЕТИРОВАНЫ:**

#### **1. Немедленно:**
```bash
# 1. Деактивируйте ключи в AWS Console
# 2. Создайте новые ключи
# 3. Обновите во всех системах
```

#### **2. Очистите Git историю:**
```bash
# Удалите ключи из всех коммитов (ОПАСНО!)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/file/with/keys' \
  --prune-empty --tag-name-filter cat -- --all
```

#### **3. Проверьте логи:**
- AWS CloudTrail
- Billing dashboard
- Подозрительную активность

### **📋 CHECKLIST БЕЗОПАСНОСТИ:**

- [ ] ✅ AWS ключи НЕ в Git репозитории
- [ ] ✅ Используются environment variables
- [ ] ✅ Ключи в CI/CD как secrets
- [ ] ✅ Ограниченные IAM права
- [ ] ✅ Регулярная ротация ключей
- [ ] ✅ Мониторинг включен
- [ ] ✅ .env файлы в .gitignore

### **🔍 КАК ПРОВЕРИТЬ:**

```bash
# Поиск ключей в Git истории
git log --all -S"AKIA" --source --all
git log --all -S"AWS_ACCESS_KEY" --source --all

# Проверка текущих файлов
grep -r "AKIA" .
grep -r "AWS_ACCESS_KEY" .
```

**🎯 ПОМНИТЕ: Безопасность AWS ключей - это ответственность разработчика!**
