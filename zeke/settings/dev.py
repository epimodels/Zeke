import os
BASE_DIR = os.path.dirname(__file__)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, "..", 'db.sqlite3'),
    }
}
DEBUG = True
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_mathjax',
)
ROOT_URLCONF = 'zeke.urls'
SECRET_KEY = os.environ.get('SECRET_KEY')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "..", "static"),
)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "..", "templates"),
)
MATHJAX_ENABLED=True