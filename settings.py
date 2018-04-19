"""
    Author: tianwei
    Email: liutianweidlut@gmail.com
    Description: Django setting base template
    Created: 2013-4-12
"""

import os
from os.path import join

SETTINGS_ROOT = os.path.dirname(__file__)

ADMINS = (('tianwei', '416774905@qq.com'),)

MANAGERS = ADMINS

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh_cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = join(SETTINGS_ROOT, 'media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = join(SETTINGS_ROOT, 'static/')
COMMON_STITICFILES_DIR = join(SETTINGS_ROOT, 'static/')

# URL prefix for static files.
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #COMMON_STITICFILES_DIR,
    MEDIA_ROOT,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'dajaxice.finders.DajaxiceFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '((8!_-pdeoo5ewkh#hm2(f^0y=ncx2)$^=#t+a$k2^&amp;7dqun1='

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'backend.custom_middlewares.PreviousURLMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_cas.middleware.CASMiddleware',
	'django.middleware.doc.XViewMiddleware',

)

ROOT_URLCONF = 'urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'wsgi.application'


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join(SETTINGS_ROOT, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.csrf',
    'django.contrib.messages.context_processors.messages',
    'context.application_settings',
    'context.userauth_settings',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    #Enhanced Admin
    'djangocms_admin_style',
    #Project
    'home',
    'adminStaff',
    'const',
    'users',
    'registration',
    'school',
    'college',
    'teacher',
    'expert',
    'finance',
    'common',
    #Add-on
    'south',
    'dajaxice',
    'dajax',
    'chartit',
)

print 'dddd'

#Add support  to user profile
ACCOUNT_ACTIVATION_DAYS = 30
LOGIN_REDIRECT_URL = '/'

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# SERVER_EMAIL = "kyywf@dlut.edu.cn"
# EMAIL_SUBJECT_PREFIX = '[ScientificResearch]'
# EMAIL_HOST = 'mail.dlut.edu.cn'
# EMAIL_PORT = '25'
# EMAIL_HOST_USER = 'kyywf@dlut.edu.cn'
# f = open('password.tmp')
# EMAIL_HOST_PASSWORD = f.read().strip()
# f.close()
# DEFAULT_FROM_EMAIL = 'kyywf@dlut.edu.cn'
# EMAIL_USE_TLS = False

# EMAIL_USER = '1911362549@mail.dlut.edu.cn'
# EMAIL_PASS = '19940308liuxiang'

EMAIL_USER = 'cxlt@dlut.edu.cn'
EMAIL_PASS = 'YL8-Aux-A9v-5Yn'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SERVER_EMAIL = EMAIL_USER
EMAIL_SUBJECT_PREFIX = '[DlutInnovationManagement]'
EMAIL_HOST = 'mail.dlut.edu.cn'
EMAIL_PORT = '25'
EMAIL_HOST_USER = EMAIL_USER
EMAIL_HOST_PASSWORD = EMAIL_PASS
DEFAULT_FROM_EMAIL = EMAIL_USER
EMAIL_USE_TLS = True

# EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
# SERVER_EMAIL = "862799735@qq.com"
# EMAIL_SUBJECT_PREFIX = '[MinzuInnovationManagement]'
# EMAIL_HOST = 'smtp.qq.com'
# EMAIL_PORT = '465'
# EMAIL_HOST_USER = '862799735@qq.com'
# EMAIL_HOST_PASSWORD = 'asd2148025'
# DEFAULT_FROM_EMAIL = '862799735@qq.com'

#########################
# File Transfer settings
PREPARE_UPLOAD_BACKEND = 'filetransfers.backends.delegate.prepare_upload'
PUBLIC_DOWNLOAD_URL_BACKEND = 'filetransfers.backends.base_url.public_download_url'
PUBLIC_DOWNLOADS_URL_BASE = '/data/'

TMP_FILE_PATH = join(SETTINGS_ROOT, 'tmp/')

LOGGING_OUTPUT_ENABLED = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler',
        },
        'console': {
            'level': 'INFO',  #here can change the debug info!
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}


# project original file
PROCESS_FILE_PATH = join("tmp", "process_file")
HOMEPAGE_PIC_PATH = join(MEDIA_ROOT, "homepage_pic")
# news documents path
NEWS_DOCUMENTS_PATH = "news-documents/%Y/%m/%d"

# tmp files path
TMP_FILES_PATH = join(MEDIA_ROOT, "tmp")

#FILE Upload
#NOTICE: the prefix 0 is important
FILE_UPLOAD_MAX_MEMORY_SIZE = 52214400
FILE_UPLOAD_PERMISSIONS = 0644
FILE_UPLOAD_TEMP_DIR = os.path.join(SETTINGS_ROOT, PROCESS_FILE_PATH).replace("\\",'/')
FILE_UPLOAD_HANDLERS = ('django.core.files.uploadhandler.MemoryFileUploadHandler',
                        'django.core.files.uploadhandler.TemporaryFileUploadHandler',
                        )
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

#chartit
CHARTIT_JS_REL_PATH = '/js/chartit-highchart/chartit/js/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas.backends.CASBackend',
)

CAS_SERVER_URL = 'https://sso.dlut.edu.cn/cas'

CAS_REDIRECT_URL = 'accounts/casredirect/'
