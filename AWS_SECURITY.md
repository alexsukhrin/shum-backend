# 🔒 AWS Security Guidelines

## ⚠️ **CRITICALLY IMPORTANT: AWS Key Security**

### **❌ NEVER DO:**

1. **Don't commit AWS keys to Git:**
   ```bash
   # ❌ BAD - any keys in code
   AWS_ACCESS_KEY = ""
   AWS_SECRET_KEY = ""
   ```

2. **Don't save in public files:**
   - README.md
   - config files in Git
   - Comments in code
   - Documentation

3. **Don't share in chats/slack:**
   - Screenshots with keys
   - Copying .env files
   - Logs with credentials

### **✅ PROPER STORAGE:**

#### **1. Local development:**
```env
# .envs/.local/.django (NOT in Git!)
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

# Or use AWS IAM Role (best option)
```

### **🛡️ BEST PRACTICES:**

#### **1. Use IAM Roles (recommended):**
```bash
# Assign IAM Role to EC2 instance instead of keys
# Then AWS SDK will automatically get credentials
```

#### **2. Limited permissions:**
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

#### **3. Key rotation:**
- Change keys every 90 days
- Use temporary keys where possible
- Delete unused keys

#### **4. Monitoring:**
- Enable CloudTrail for logging
- Set up alerts for suspicious activity
- Check Access Logs regularly

### **🚨 WHAT TO DO IF KEYS ARE COMPROMISED:**

#### **1. Immediately:**
```bash
# 1. Deactivate keys in AWS Console
# 2. Create new keys
# 3. Update in all systems
```

#### **2. Clean Git history:**
```bash
# Remove keys from all commits (DANGEROUS!)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/file/with/keys' \
  --prune-empty --tag-name-filter cat -- --all
```

#### **3. Check logs:**
- AWS CloudTrail
- Billing dashboard
- Suspicious activity

### **📋 SECURITY CHECKLIST:**

- [ ] ✅ AWS keys NOT in Git repository
- [ ] ✅ Using environment variables
- [ ] ✅ Keys in CI/CD as secrets
- [ ] ✅ Limited IAM permissions
- [ ] ✅ Regular key rotation
- [ ] ✅ Monitoring enabled
- [ ] ✅ .env files in .gitignore

### **🔍 HOW TO CHECK:**

```bash
# Search for keys in Git history
git log --all -S"AKIA" --source --all
git log --all -S"AWS_ACCESS_KEY" --source --all

# Check current files
grep -r "AKIA" .
grep -r "AWS_ACCESS_KEY" .
```

**🎯 REMEMBER: AWS key security is the developer's responsibility!**
