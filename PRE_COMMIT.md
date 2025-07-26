# Pre-commit Setup and Usage

## 📋 Pre-commit is installed and configured!

Pre-commit automatically checks and fixes code before each commit.

## 🛠️ What pre-commit does:

### **1. Basic checks:**
- Removes trailing whitespace
- Adds empty line at end of files
- Checks JSON, YAML, TOML syntax
- Finds debug statements
- Detects private keys

### **2. Python code:**
- **Django-upgrade** - updates code for Django 5.0
- **Ruff** - linter and formatter (replaces flake8 + black)
- Automatically fixes code style

### **3. Django templates:**
- **djLint** - formats and checks HTML templates
- Fixes indentation and structure

## 🚀 Usage:

### **Automatically on commit:**
```bash
git add .
git commit -m "Your message"
# Pre-commit will run automatically
```

### **Manual run:**
```bash
# On all files
pre-commit run --all-files

# Only on changed files
pre-commit run

# Specific hook
pre-commit run ruff-check
```

### **In Docker container:**
```bash
# Run in Django container
docker-compose -f docker-compose.local.yml exec django pre-commit run --all-files
```

## ⚠️ If pre-commit "fails":

### **1. Automatic fixes:**
If pre-commit fixed files:
```bash
git add .
git commit -m "Your message"  # Try again
```

### **2. Skip pre-commit (not recommended):**
```bash
git commit -m "Your message" --no-verify
```

### **3. Fix manually:**
Look at the errors and fix them according to the messages.

## 🔧 Setup for developers:

### **Local installation:**
```bash
# 1. Install pre-commit
pip install pre-commit

# 2. Install hooks
pre-commit install

# 3. Run on all files (first time)
pre-commit run --all-files
```

### **Update hooks:**
```bash
pre-commit autoupdate
```

## 📁 Configuration:

Settings in `.pre-commit-config.yaml` file:
- **exclude**: ignore docs/, migrations/, devcontainer.json
- **Python 3.12** by default
- **Django 5.0** compatibility

## ✅ In CI/CD:

GitHub Actions automatically runs pre-commit:
- On each Pull Request
- On push to main/master
- Checks code quality

## 🎯 Recommendations:

1. **Don't disable pre-commit** - it helps maintain quality
2. **Regularly update** hooks with `pre-commit autoupdate`
3. **Fix errors** instead of ignoring them
4. **Commit more often** - easier to fix errors

## 🚫 What to do with problems:

### **If it hangs:**
```bash
pre-commit clean
pre-commit install --install-hooks
```

### **If you need to update settings:**
```bash
pre-commit autoupdate
pre-commit run --all-files
```

**Pre-commit will help maintain code in excellent condition! 🎉**
