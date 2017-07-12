DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SECRET_KEY = 'fake-key'

INSTALLED_APPS = [
    'csv_export',
    'tests',
]

USE_TZ = True

ROOT_URLCONF = 'tests.urls'
