# Imports
import os
import django_heroku
from pathlib import Path
from dotenv import load_dotenv
from decouple import config



# Loading dotenv ------------
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="django-insecure-ii@h9lsa#%3+$tqvys-d0rma0k47ia5e20o94okam$)983y39q")



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=True, cast=bool)


# Allowed hosts
ALLOWED_HOSTS = ['https://company-assessments-85bd491e25c3.herokuapp.com', 'http127.0.0.1', 'http://localhost']


# Application definition ----
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

LOCAL_APPS = [
    'apps',
    'apps.user',
    'apps.auth',
    'apps.logs',
    'apps.element',
    'apps.companies',
    'apps.countries',
    'apps.continents',
    'apps.regions',
    'apps.industries',
    'apps.supersectors',
    'apps.sectors',
    'apps.subsectors',
    'apps.evaluations',
    'apps.relations',
    'apps.relations_tree',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
]
    
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS


# Middleware ----------------
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

ROOT_URLCONF = 'CompanyRest.urls'


# Templates -----------------
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

WSGI_APPLICATION = 'CompanyRest.wsgi.application'


# Databases -----------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config("DATABASE_NAME", 'd9t51qosamg0dv'), 
        'USER': config("DATABASE_USER", default="u6b5t400ij4ji1"),
        'PASSWORD': config("DATABASE_PASSWORD", 'pec824a22933f50289136a47c9e4546e80851503a66db43f3f195043bbd603865'), 
        'HOST': config("DATABASE_HOST", 'c8m0261h0c7idk.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com'),  
        'PORT': config("DATABASE_PORT", '5432'), 
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_FILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# Django Heroku settings ----
django_heroku.settings(locals()) 


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# User model ----------------
AUTH_USER_MODEL = 'apps_user.User'


# Rest Frameworks -----------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    #'DEFAULT_PAGINATION_CLASS':'rest_framework.pagination.LimitOffsetPagination',
    #'PAGE_SIZE':15,
}



# Geo ip path ---------------
GEOIP_PATH = BASE_DIR / 'geoip'





# Cors headers --------------
#CORS_ALLOW_CREDENTIALS = True


CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

#CSRF_COOKIE_HTTPONLY = True
#SESSION_COOKIE_HTTPONLY = True

#SESSION_COOKIE_SAMESITE = 'None'
#CSRF_COOKIE_SAMESITE = 'None'

CORS_DEFAULT_ORIGINS = 'https://react-standalone-app-465feb572a17.herokuapp.com','http://localhost:3000,http://127.0.0.1:3000'

CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", default=CORS_DEFAULT_ORIGINS ).split(",")


#CSRF_COOKIE_NAME = 'XSRF-TOKEN'
#CSRF_HEADER_NAME = 'HTTP_X_XSRF_TOKEN'
