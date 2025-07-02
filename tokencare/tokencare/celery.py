# tokencare/celery.py
import os
from celery import Celery

# Set default Django settings
# DJANGO_SETTINGS_MODULE is a django LazySetting object that loads settings.py when needed
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tokencare.settings') 
# This line ensures that celery is aware of django settings becuase both are different and need to know each other's configurations to work togehter

# here tokencare is the name of celery app which we use in the command celery -A tokencare worker
app = Celery('tokencare')

# Tells Celery to read all CELERY_... keys from Django's settings.py.
app.config_from_object('django.conf:settings', namespace='CELERY')
# Celery uses import_string() or similar logic to import an object from a module.
# The colon : is shorthand to say: "Import the settings object from inside django.conf"
# This is equivalent to:
# from django.conf import settings
# app.config_from_object(settings)

# Looks in all installed apps for a tasks.py and auto-registers tasks from there.
app.autodiscover_tasks()