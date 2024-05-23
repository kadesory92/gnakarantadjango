import os
from dotenv import load_dotenv

# Récupération du répertoire parent du fichier actuel
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Chargement des variables d'environnement depuis le fichier .env
# load_dotenv('config.dev.env')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-*b+9yl3s5qt=8n-)0&^18d!@)&31sd^+)iwr*^=l%9a9u+b^2+'
#
# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'account.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'core',
    'messaging',
    'school',
    'service',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gnkaranta.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'account', 'templates'),
            os.path.join(BASE_DIR, 'core', 'templates'),
            os.path.join(BASE_DIR, 'service', 'templates'),
            os.path.join(BASE_DIR, 'school', 'templates'),
            os.path.join(BASE_DIR, 'messaging', 'templates'),
        ],
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

WSGI_APPLICATION = 'gnkaranta.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Paramètres de base de données
# DEBUG = os.getenv('DEBUG', 'True') == 'True'
DEBUG = 'True'
SECRET_KEY = 'django-insecure-*b+9yl3s5qt=8n-)0&^18d!@)&31sd^+)iwr*^=l%9a9u+b^2+'
# SECRET_KEY = os.getenv('SECRET_KEY')
# DB_NAME = os.getenv('DB_NAME')
# DB_USER = os.getenv('DB_USER')
# DB_PASSWORD = os.getenv('DB_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Modification du moteur de base de données
        'NAME': 'db_gnkaranta',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',  # 'localhost',
        'PORT': '3306',  # Port par défaut de MySQL
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',  # Modification du moteur de base de données
#         'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('HOST'),  # 'localhost',
#         'PORT': '3306',  # Port par défaut de MySQL
#     }
# }

# URL de l'application
# APP_URL = os.getenv('APP_URL', 'http://localhost:8000')
APP_URL = 'http://localhost:8000'


# Paramètres de messagerie électronique
# EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
# EMAIL_PORT = int(os.getenv('EMAIL_PORT', 25))
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'False') == 'True'

# Configuration du stockage des fichiers statiques
# STATIC_URL = os.getenv('STATIC_URL', "static/")
# STATIC_ROOT = os.getenv('STATIC_ROOT', "static/")


# Configuration du stockage des fichiers téléchargés
# MEDIA_URL = os.getenv('MEDIA_URL', "media/")
# MEDIA_ROOT = os.getenv('MEDIA_ROOT', "media/")

# Configuration de langue par défaut
# LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'en-us')

# Configuration du fuseau horaire
# TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')

# Active la traduction internationale
# USE_I18N = os.getenv('USE_I18N', 'True') == 'True'

# Active le support des fuseaux horaires
# USE_TZ = os.getenv('USE_TZ', 'True') == 'True'

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
#
TIME_ZONE = 'UTC'
#
USE_I18N = True
#
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# URL et répertoire pour les fichiers médias
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
