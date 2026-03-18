# Complete Render Deployment Guide for Django Projects

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Database Configuration](#database-configuration)
4. [Static & Media Files](#static--media-files)
5. [Environment Variables](#environment-variables)
6. [Deployment Steps](#deployment-steps)
7. [Common Problems & Solutions](#common-problems--solutions)
8. [Maintenance & Updates](#maintenance--updates)
## Prerequisites

### Required Accounts:
- ✅ GitHub account
- ✅ Render account (free tier available)
- ✅ Cloudinary account (free tier for images)

### Local Setup:
```bash
# Install required packages
pip install django gunicorn psycopg2-binary dj-database-url whitenoise cloudinary django-cloudinary-storage python-decouple

---

# **SECTION 3: Database Configuration**

Copy this third block:

```markdown
## Database Configuration

### settings.py Database Setup:
```python
import dj_database_url
import os

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}",
        conn_max_age=600,
    )
}

---

# **SECTION 4: Static & Media Files with Cloudinary**

Copy this fourth block:

```markdown
## Static & Media Files

### Static Files Configuration:
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# In INSTALLED_APPS
INSTALLED_APPS = [
    # ...
    'cloudinary_storage',
    'cloudinary',
    'portfolio_site.main',
]

# Cloudinary configuration
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

# Force Cloudinary in production
if 'RENDER' in os.environ:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

---

# **SECTION 5: Environment Variables**

Copy this fifth block:

```markdown
## Environment Variables

### Local (.env file):
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost
Email (if needed)

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
Cloudinary (get from cloudinary.com)

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

### Render Dashboard (Required Variables):
SECRET_KEY=your_production_secret_key
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com,www.yourdomain.com
CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com
DATABASE_URL=auto-filled by Render
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=your@email.com
DJANGO_SUPERUSER_PASSWORD=secure_password
## Deployment Steps

### 1. **Create build.sh**
```bash
#!/bin/bash
# Exit on error
set -o errexit

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
#make it executable
chmod +x build.sh
#create custom admin command
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Ensures an admin user exists'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        
        if username and password and email:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username, email, password)
                self.stdout.write(self.style.SUCCESS(f'Superuser created'))
#requirements.txt
asgiref==3.9.1
Django==5.2.6
gunicorn==25.1.0
psycopg2-binary==2.9.11
dj-database-url==1.2.0
whitenoise==6.5.0
python-decouple==3.8
cloudinary==1.36.0
django-cloudinary-storage==0.3.0
pillow==11.3.0
#render dashboard configuration
Setting	Value
Build Command	./build.sh
Start Command	python manage.py ensure_adminuser && gunicorn portfolio_site.wsgi:application --bind 0.0.0.0:$PORT --log-file -
#common problems and solutions
### **PROBLEM 1: "relation does not exist" Error**
**Solution:**
bash
# Add migrations to build command
python manage.py makemigrations
python manage.py migrate
#image disappear after deploy
# Use os.environ.get() NOT config()
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

# Force Cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
#problem 3
#migration conflicts
# Check migration dependencies
python manage.py showmigrations

# Fix by ensuring dependencies are correct
# In your migration file:
dependencies = [
    ('main', '0005_previous_migration_name'),
]

# Or merge:
python manage.py makemigrations --merge

---

# **SECTION 8: Common Problems & Solutions (Part 2)**

Copy this eighth block:

```markdown
### **PROBLEM 4: Static Files Not Loading**

**Symptoms:**
- CSS/JS missing
- 404 errors for static files

**Solution:**
```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# MIDDLEWARE must include WhiteNoise (order matters!)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Right after security
    # ...
]

---

# **SECTION 9: Common Problems & Solutions (Part 3)**

Copy this ninth block:

```markdown
### **PROBLEM 7: Environment Variables Not Reading**

**Symptoms:**
- Cloudinary not working
- Variables show as None

**Solution:**
```python
# Use os.environ.get() NOT config() for Render
CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')

# Debug: Add test view
def test_env(request):
    return JsonResponse({
        'cloud_name': os.environ.get('CLOUDINARY_CLOUD_NAME'),
        'api_key_exists': bool(os.environ.get('CLOUDINARY_API_KEY')),
    })
#500 internal error
# Temporarily enable debug to see error
DEBUG = True  # Just for debugging!

# Check Render logs for traceback
# Common causes: missing env vars, database connection issues

---

# **SECTION 10: Debugging Toolkit**

Copy this tenth block:

```markdown
## Debugging Toolkit

### 1. **Test Cloudinary Connection**
```python
# test_cloudinary.py
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_site.settings')
django.setup()

from cloudinary import uploader

try:
    result = uploader.upload(
        "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
        public_id="test"
    )
    print("✅ Cloudinary working!")
    print(f"URL: {result['url']}")
except Exception as e:
    print(f"❌ Failed: {e}")

---

# **SECTION 11: Data Migration for Existing Projects**

Copy this eleventh block:

```markdown
## Data Migration for Existing Projects

### Export from Local SQLite:
```bash
python manage.py dumpdata main.Project --indent 4 > main/fixtures/projects_fixture.json

---

# **SECTION 12: Maintenance & Final Checklist**

Copy this twelfth and final block:

```markdown
## Maintenance & Updates

### Adding New Projects (After Cloudinary Setup):
1. Go to `https://your-app.onrender.com/admin`
2. Click "Add Project"
3. Fill details and upload image
4. Image automatically goes to Cloudinary
5. **No redeploy needed!**

### Code Updates:
```bash
git add .
git commit -m "Description of changes"
git push origin main
# Render auto-deploys
