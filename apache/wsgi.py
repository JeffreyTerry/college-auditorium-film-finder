import os
import sys	
sys.path.append('~/dankswank/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'dankswank.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
