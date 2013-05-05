import os
import dj_database_url
from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

default_db_url = 'sqlite:///%s' % os.path.join(os.path.dirname(__file__), '..', '..', '..', 'limetime.db3')
DATABASES = {'default': dj_database_url.config(default=default_db_url)}

INTERNAL_IPS = ('127.0.0.1', '192.168.0.1', '0.0.0.0')
INSTALLED_APPS.append('debug_toolbar')
MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

def custom_show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': custom_show_toolbar,
    'EXTRA_SIGNALS': [],
    'HIDE_DJANGO_SQL': True,
    'TAG': 'div',
    'ENABLE_STACKTRACES' : True,
}
