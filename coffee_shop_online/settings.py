import os
from pathlib import Path
from datetime import timedelta
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET-KEY', default='django-insecure-ou&ce5w$r9c5fry+p*5f5h^jfsg)key^r^qfez&6%v4+*1jm@l')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,0.0.0.0').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

	# Сторонние приложения
	'rest_framework',           # Django REST Framework
	'rest_framework_simplejwt', # JWT аутентификация
	'corsheaders',              # CORS headers для фронтенда
	'drf_yasg',                 # Swagger документация
	'django_filters',           # Фильтрация

	# Локальные приложения
	'api',
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

ROOT_URLCONF = 'coffee_shop_online.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'coffee_shop_online.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# Настройки БД
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.getenv('DB_NAME', 'coffee_shop_db'),
		'USER': os.getenv('DB_USER', 'coffee_user'),
		'PASSWORD': os.getenv('DB_PASSWORD', 'coffee_password'),
		'HOST': os.getenv('DB_HOST', 'db'),  # 'db' для Docker
		'PORT': os.getenv('DB_PORT', '5432'),
	}
}

# Для разработки можно использовать SQLite
#if config('USE_SQLITE', default=False, cast=bool):
#	DATABASES = {
#		'default': {
#			'ENGINE': 'django.db.backends.sqlite3',
#			'NAME': BASE_DIR / 'db.sqlite3',
#		}
#	}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки REST Framework
REST_FRAMEWORK = {
	# Классы аутентификации - JWT будет основным
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework_simplejwt.authentication.JWTAuthentication',
	),
	# Права доступа по умолчанию
	'DEFAULT_PERMISSION_CLASSES': (
		'rest_framework.permissions.IsAuthenticatedOrReadOnly',  # Чтение для всех, запись для авторизованных
	),
	# Пагинация для всех списковых endpoints
	'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
	'PAGE_SIZE': 10  # 10 элементов на страницу
}

# Настройки JWT токенов
SIMPLE_JWT = {
	'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),   # Время жизни access токена
	'REFRESH_TOKEN_LIFETIME': timedelta(days=1),      # Время жизни refresh токена
	'ROTATE_REFRESH_TOKENS': False,
	'BLACKLIST_AFTER_ROTATION': True,
}

# CORS настройки для фронтенда
CORS_ALLOWED_ORIGINS = [
	"http://localhost:3000",  # React dev server
	"http://127.0.0.1:3000",
	"http://localhost:8080",  # Vue.js dev server
	"http://127.0.0.1:8080",
]
CORS_ALLOW_CREDENTIALS = True  # Разрешить передачу cookies

# Настройки Swagger для документации API
SWAGGER_SETTINGS = {
	'SECURITY_DEFINITIONS': {
		'Bearer': {
			'type': 'apiKey',
			'name': 'Authorization',
			'in': 'header'
		}
	},
	'USE_SESSION_AUTH': False,  # Отключаем сессионную аутентификацию в Swagger
}
