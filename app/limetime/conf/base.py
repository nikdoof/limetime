import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(os.path.dirname(__file__), '..', 'static'),
    ]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = [
    os.path.join(os.path.dirname(__file__), '..', 'templates'),
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'gunicorn',
    'timer',
]

SITE_ID = 1
ROOT_URLCONF = 'limetime.urls'
WSGI_APPLICATION = 'limetime.wsgi.application'
SECRET_KEY = '$+y3w%y3286wetd#tqhvqch$^ed)x=#s$we1c2)d1&lf9quktl'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
