# Pre-commit Setup and Usage

## 📋 Pre-commit установлен и настроен!

Pre-commit автоматически проверяет и исправляет код перед каждым коммитом.

## 🛠️ Что делает pre-commit:

### **1. Базовые проверки:**
- Удаляет trailing whitespace
- Добавляет пустую строку в конец файлов
- Проверяет JSON, YAML, TOML синтаксис
- Находит debug statements
- Обнаруживает приватные ключи

### **2. Python код:**
- **Django-upgrade** - обновляет код под Django 5.0
- **Ruff** - линтер и форматтер (заменяет flake8 + black)
- Автоматически исправляет стиль кода

### **3. Django шаблоны:**
- **djLint** - форматирует и проверяет HTML шаблоны
- Исправляет отступы и структуру

## 🚀 Использование:

### **Автоматически при коммите:**
```bash
git add .
git commit -m "Your message"
# Pre-commit автоматически запустится
```

### **Запуск вручную:**
```bash
# На всех файлах
pre-commit run --all-files

# Только на изменённых файлах
pre-commit run

# Конкретный hook
pre-commit run ruff-check
```

### **В Docker контейнере:**
```bash
# Запуск в Django контейнере
docker-compose -f docker-compose.local.yml exec django pre-commit run --all-files
```

## ⚠️ Если pre-commit "падает":

### **1. Автоматические исправления:**
Если pre-commit исправил файлы:
```bash
git add .
git commit -m "Your message"  # Попробуйте снова
```

### **2. Пропустить pre-commit (не рекомендуется):**
```bash
git commit -m "Your message" --no-verify
```

### **3. Исправить вручную:**
Посмотрите на ошибки и исправьте их согласно сообщениям.

## 🔧 Настройка для разработчиков:

### **Установка локально:**
```bash
# 1. Установить pre-commit
pip install pre-commit

# 2. Установить hooks
pre-commit install

# 3. Запустить на всех файлах (первый раз)
pre-commit run --all-files
```

### **Обновление hooks:**
```bash
pre-commit autoupdate
```

## 📁 Конфигурация:

Настройки в файле `.pre-commit-config.yaml`:
- **exclude**: игнорируем docs/, migrations/, devcontainer.json
- **Python 3.12** по умолчанию
- **Django 5.0** совместимость

## ✅ В CI/CD:

GitHub Actions автоматически запускает pre-commit:
- При каждом Pull Request
- При push в main/master
- Проверяет качество кода

## 🎯 Рекомендации:

1. **Не отключайте pre-commit** - он помогает поддерживать качество
2. **Регулярно обновляйте** hooks командой `pre-commit autoupdate`
3. **Исправляйте ошибки** вместо их игнорирования
4. **Коммитьте чаще** - так проще исправлять ошибки

## 🚫 Что делать при проблемах:

### **Если зависло:**
```bash
pre-commit clean
pre-commit install --install-hooks
```

### **Если нужно обновить настройки:**
```bash
pre-commit autoupdate
pre-commit run --all-files
```

**Pre-commit поможет поддерживать код в отличном состоянии! 🎉**
