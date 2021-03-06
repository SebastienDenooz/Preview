# -*- coding: utf-8 -*-
# Django settings for font_viewer project.
import os
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'font_viewer.db',                      # Or path to database file if using sqlite3.
#        'USER': '',                      # Not used with sqlite3.
#        'PASSWORD': '',                  # Not used with sqlite3.
#        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
#    }

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'fontviewer',                      # Or path to database file if using sqlite3.
        'USER': 'fontviewer',                      # Not used with sqlite3.
        'PASSWORD': 'fontviewer',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, "../static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'l^v&amp;&amp;m59p!=+1)^n+2sx$fj4w@@ms)exu-_$400-faw+1@dv-='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'font_viewer.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'font_viewer.wsgi.application'

TEMPLATE_DIRS = ('/home/sebastien/Développement/font_viewer/templates',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'font_manager',
    'django_extensions',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'datesimple': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'log_to_stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'datesimple',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        '': {
            'handlers': ['log_to_stdout'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

FONT_FILE_PATH = "/home/sebastien/Fonts"
THUMBNAIL_FILE_PATH = "/home/sebastien/Images/Thumb"
THUMBNAIL_CREATED_BY_PASS = 50
PREVIEWS_BY_PAGE = 50
FONT_FORMATS = (
    # ('File ext', 'MimeType')
    ('.eot', 'application/vnd.ms-fontobject'),
    ('.pfb', 'application/octet-stream'),
    ('.ttf', 'application/x-font-ttf'),
    ('.pfm', 'application/octet-stream'),
    ('.fon', 'application/x-dosexec'),
    ('.woff', 'application/octet-stream'),
    ('.svg', 'image/svg+xml'),
)
THUMBNAIL_FORMAT = (
    # ('name', 'Demo text', 'x','y')
    ('tiny', 'Aa', 80,80),
    ('big', u'Mes Aïeux mélomane !', 400, 100),
    ('text',u"""
Oui alors écoute moi, je suis mon
meilleur modèle car en vérité, la vérité,
il n'y a pas de vérité parce que
spirituellement, on est tous ensemble, ok ?
Il y a un an, je t'aurais
parlé de mes muscles.

Ça sounds good, je ne suis pas
un simple danseur car il faut
se recréer... pour recréer...
a better you et c'est une sensation
réelle qui se produit si on veut ! Tu vas te dire :
J'aurais jamais cru que
le karaté guy pouvait parler comme ça !

Quand tu fais le calcul,
si vraiment tu veux te
rappeler des souvenirs
de ton perroquet, c'est
un très, très gros travail et je ne
cherche pas ici à mettre un point !
Ça respire le meuble de Provence, hein ?
""", 800, 600)
)
# Time in second
UPDATE_FREQUENCY = 60*60*24*7
# Minimum number of files to be indexed during a pass
MINIMUM_NUMBER_FILES_TO_INDEX = 20000