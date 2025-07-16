from .celery import app as celery_app

__all__ = ('celery_app',)

# this allows celery to be discovered when you run celery -A tokencare worker --loglevel=info
# Celery knows that it has to load celery_app from your project’s __init__.py.
# This makes your Celery app available when Django starts up — so that: celery -A tokencare worker can find and load your Celery app from tokencare/__init__.py.

from patients import tasks