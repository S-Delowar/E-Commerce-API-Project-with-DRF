import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


import environ
env = environ.Env()
ENVIRONMENT = env('DJANGO_EVN', default='development')
if ENVIRONMENT == 'production':
    environ.Env.read_env(os.path.join(BASE_DIR, '.env.prod'))
else:
    environ.Env.read_env(os.path.join(BASE_DIR, '.env.dev'))



SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env('DJANGO_DEBUG', default=False)
ALLOWED_HOSTS = env('DJANGO_ALLOWED_HOSTS').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # third party
    'rest_framework',
    'rest_framework.authtoken',
    
    'dj_rest_auth',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    
    'corsheaders',
    'drf_spectacular',
    # local
    'accounts',
    'shop',
    'cart',
    'order',
    'payment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # CORS
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # allauth
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'ecommerce_api_project.urls'

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

WSGI_APPLICATION = 'ecommerce_api_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': env.db()
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR,]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Setup Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'



# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

REST_USE_JWT = True

# JWT configuration
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Schema and Documentation
SPECTACULAR_SETTINGS = {
    'TITLE': 'E-commerce API Project',
    'DESCRIPTION': 'A simple e-commerce backend project',
    'VERSION': '1.0.0',
}


# Django AllAuth
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_VERIFICATION = 'optional'


# CORS
CORS_ALLOWED_ORIGINS = [
    # "https://sub.example.com",
    "http://localhost:3000",
    "http://localhost:8080",
]

# CSRF
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
]


# Deployment Checklist
SECURE_SSL_REDIRECT=env.bool('DJANGO_SECURE_SSL_REDIRECT', default=True)
SECURE_HSTS_SECONDS=env.int('DJANGO_SECURE_HSTS_SECONDS', default=2592000)
SECURE_HSTS_INCLUDE_SUBDOMAINS=env.bool('DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True)
SECURE_HSTS_PRELOAD=env.bool('DJANGO_SECURE_HSTS_PRELOAD', default=True)
SESSION_COOKIE_SECURE=env.bool('DJANGO_SESSION_COOKIE_SECURE', default=True)
CSRF_COOKIE_SECURE=env.bool('DJANGO_CSRF_COOKIE_SECURE', default=True)


# Payment Getway
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY =env('STRIPE_PUBLISHABLE_KEY')

