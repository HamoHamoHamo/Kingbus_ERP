import os
import logging
import my_settings
from pathlib import Path
from os.path import join
from datetime import datetime

TODAY = str(datetime.now())[:10]
FORMAT = "%Y-%m-%d"
VERSION = my_settings.VERSION

SERVER_ENV = os.environ.get("DJANGO_SETTINGS_MODULE", "config.settings.base")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = my_settings.SECRET_KEY

# 팝빌 계좌조회
LinkID = my_settings.LinkID
SecretKey = my_settings.SecretKey
IsTest = my_settings.IsTest
IPRestrictOnOff = my_settings.IPRestrictOnOff
UseStaticIP = my_settings.UseStaticIP
UseLocalTimeYN = my_settings.UseLocalTimeYN


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
APPEND_SLASH = False


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
    'django.contrib.humanize',

    'crudmember.apps.CrudmemberConfig',
    'notice.apps.NoticeConfig',
    'accounting.apps.AccountingConfig',
    'dispatch.apps.DispatchConfig',
    'accident.apps.AccidentConfig',
    'humanresource.apps.HumanresourceConfig',
    'vehicle.apps.VehicleConfig',
    'homepage',
    'document',
    'complaint',
    'assignment',
    'salary',
    "debug_toolbar",
    'approval',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'static.middleware.LoginCheckMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = my_settings.DATABASES

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://localhost:6379',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'TIMEOUT': 60 * 60 * 24 * 7,  # 기본 만료 시간 7일
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
# STATIC_DIR = os.path.join(BASE_DIR, 'static')
#STATICFILES_FINDERS = ['django.contrib.staticfiles.finders.FileSystemFinder',]
STATICFILES_DIRS=[
    os.path.join(BASE_DIR, 'static')
#     os.path.join(BASE_DIR,'crudmember','static'),
#     os.path.join(BASE_DIR,'accounting','static'),
#     os.path.join(BASE_DIR,'dispatch','static'),
#     os.path.join(BASE_DIR,'document','static'),
#     os.path.join(BASE_DIR,'humanresource','static'),
    # os.path.join(BASE_DIR,'vehicle','static'),
#     os.path.join(BASE_DIR,'notice','static'),
    
]

# collectstatic 명령어가 실행되면 이 경로로 static 파일이 복사됨
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 미디어 파일을 관리할 루트 media 디렉터리
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# 각 media file에 대한 URL prefix
MEDIA_URL = '/media/'


EMAIL_HOST = 'smtp.gmail.com'
# 메일을 호스트하는 서버
EMAIL_PORT = '587'
# gmail과의 통신하는 포트
EMAIL_HOST_USER = 'linkatnoreply@gmail.com'
# 발신할 이메일
EMAIL_HOST_PASSWORD = 'kingbus!@'
# 발신할 메일의 비밀번호
EMAIL_USE_TLS = True
# TLS 보안 방법
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# 사이트와 관련한 자동응답을 받을 이메일 주소,'webmaster@localhost'

PASSWORD_RESET_TIMEOUT = 300

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INTERNAL_IPS = [
    "127.0.0.1",
]

CRONJOBS = [
    ('* * * * *', 'dispatch.notification.driver_check_notification', '>> /home/kingbus/trp/data_backup/cpu_log/noti_`date +\%Y\%m\%d`.log 2>&1'),
    ('* * * * *', 'dispatch.notification.admin_station_check_problem_notification', '>> /home/kingbus/trp/data_backup/cpu_log/noti_`date +\%Y\%m\%d`.log 2>&1'),
    ('*/30 9-18 * * 1-5', 'dispatch.notification.admin_dispatch_check_notification', '>> /home/kingbus/trp/data_backup/cpu_log/noti_`date +\%Y\%m\%d`.log 2>&1'),
    ('0 9-18 * * 1-5', 'dispatch.notification.admin_complete_check_notification', '>> /home/kingbus/trp/data_backup/cpu_log/noti_`date +\%Y\%m\%d`.log 2>&1'),
]

from config.custom_logging import *