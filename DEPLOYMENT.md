# 🚀 Deployment Guide - Library Management System API

## Heroku Deployment

### Prerequisites
- Heroku CLI installed
- Git repository initialized
- Heroku account created

### Step 1: Prepare for Deployment

1. **Create Procfile**
```bash
echo "web: gunicorn Law_Study_AssistantAPI.wsgi --log-file -" > Procfile
```

2. **Add Gunicorn to requirements.txt**
```bash
echo "gunicorn==21.2.0" >> requirements.txt
```

3. **Update settings for production** (already configured in your project)

### Step 2: Deploy to Heroku

1. **Login to Heroku**
```bash
heroku login
```

2. **Create Heroku app**
```bash
heroku create your-library-api-name
```

3. **Set environment variables**
```bash
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="your-app-name.herokuapp.com"
```

4. **Deploy the application**
```bash
git add .
git commit -m "Deploy Library Management System API"
git push heroku main
```

5. **Run migrations**
```bash
heroku run python manage.py migrate
```

6. **Create superuser (optional)**
```bash
heroku run python manage.py createsuperuser
```

7. **Populate sample data**
```bash
heroku run python manage.py populate_library_data
```

### Step 3: Test Deployment

Your API will be available at: `https://your-app-name.herokuapp.com/`

**Key Endpoints:**
- API Documentation: `https://your-app-name.herokuapp.com/api/docs/`
- Register: `POST https://your-app-name.herokuapp.com/auth/register/`
- Login: `POST https://your-app-name.herokuapp.com/auth/login/`
- Books: `GET https://your-app-name.herokuapp.com/library/books/`

## PythonAnywhere Deployment

### Step 1: Upload Code
1. Upload your project files to PythonAnywhere
2. Extract in your home directory

### Step 2: Create Web App
1. Go to Web tab in PythonAnywhere dashboard
2. Create new web app (Django)
3. Set Python version to 3.8+

### Step 3: Configure WSGI
Update `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
```python
import os
import sys

path = '/home/yourusername/Law_Study_AssistantAPI'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'Law_Study_AssistantAPI.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 4: Install Dependencies
```bash
pip3.8 install --user -r requirements.txt
```

### Step 5: Configure Database
```bash
python3.8 manage.py migrate
python3.8 manage.py createsuperuser
python3.8 manage.py populate_library_data
```

## Environment Variables

Create `.env` file with:
```env
SECRET_KEY=your-django-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,your-app.herokuapp.com
DATABASE_URL=your-database-url-if-using-postgres
```

## Security Checklist

- ✅ DEBUG=False in production
- ✅ Strong SECRET_KEY
- ✅ ALLOWED_HOSTS configured
- ✅ HTTPS enabled
- ✅ Database secured
- ✅ Static files served properly

## API Testing

Use the provided `test_api.py` script:
```bash
python test_api.py
```

Update the BASE_URL in the script to your deployed URL.

## Monitoring

- Check Heroku logs: `heroku logs --tail`
- Monitor API performance
- Set up error tracking (optional)

## Scaling

For production use:
- Use PostgreSQL database
- Add Redis for caching
- Implement rate limiting
- Add monitoring and logging
- Set up CI/CD pipeline