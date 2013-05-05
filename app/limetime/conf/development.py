import os
import dj_database_url
from .base import *

default_db_url = 'sqlite:///%s' % os.path.join(os.path.dirname(__file__), '..', '..', '..', 'limetime.db3')
DATABASES = {'default': dj_database_url.config(default=default_db_url)}
