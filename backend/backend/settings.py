import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'your-secret-key'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'jazzmin',
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_celery_beat',
    
    'tasks.apps.TasksConfig',
    'accounts',
    'projects',
    'chat',
    'ratings',
    # "django_rq",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'
ASGI_APPLICATION = 'backend.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# CORS_ALLOW_ALL_ORIGINS = True

TELEGRAM_BOT_TOKEN = "8040016996:AAGRy-acyXz_Y3UwdJINC4oxsphE39BgeyE"

# RQ_QUEUES = {
#     "default": {
#         "HOST": "localhost",
#         "PORT": 6379,
#         "DB": 0,
#         "DEFAULT_TIMEOUT": 360, 
#     },
# }

# CELERY sozlamalari
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
print(CELERY_TASK_SERIALIZER)
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'mark-overdue-tasks-daily': {
        'task': 'tasks.tasks.mark_overdue_tasks',
        'schedule': crontab(minute='*/1'), #'schedule': crontab(hour=0, minute=0),  # har kuni soat 00:00 da ishga tushadi
    },
}

# Agar celery-beat ishlatsa:
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'


JAZZMIN_SETTINGS = {
    "site_title": "Your Admin Panel",
    "site_header": "Your Company",
    "site_brand": "Your Brand",
    "site_logo": "images/admin-logo.png",
    "login_logo": "images/login-logo.png",
    "welcome_sign": "Xush kelibsiz! Admin panelga kirish",
    "copyright": "Your Company",
    
    "order_with_respect_to": [
        "accounts", 
        "projects",
        "tasks",
        "chat",
        "ratings"
    ],
    
    "icons": {
        # Accounts app
        "accounts.User": "fas fa-user",
        "auth.Group": "fas fa-users",
        
        # Projects app
        "projects.Project": "fas fa-project-diagram",
        
        # Tasks app
        "tasks.Task": "fas fa-tasks",
        "tasks.Status": "fas fa-list-ol",
        
        # Chat app
        "chat.ChatRoom": "fas fa-comments",
        "chat.Message": "fas fa-comment",
        
        # Ratings app
        "ratings.Rating": "fas fa-star",
    },
    
    "related_modal_active": True,
    "custom_css": "css/admin-custom.css",
    "custom_js": "js/admin-custom.js",
    "show_ui_builder": True,
}