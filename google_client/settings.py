
import os
import json
from django.core.exceptions import ImproperlyConfigured

def _require_env(name):
    """Raise an error if the environment variable isn't defined"""
    value = os.getenv(name)
    if value is None:
        raise ImproperlyConfigured('Required environment variable "{}" is not set.'.format(name))
    return value

google_secret_file = json.loads(_require_env('GOOGLE_CREDENTIALS'))

GOOGLE_OAUTH2_CLIENT_ID = google_secret_file['web']['client_id']
GOOGLE_OAUTH2_CLIENT_SECRET = google_secret_file['web']['client_secret']
GOOGLE_OAUTH2_PROJECT_ID = google_secret_file['web']['project_id']

BASE_BACKEND_URL="http://localhost:8000"
BASE_FRONTEND_URL="http://localhost:3000"