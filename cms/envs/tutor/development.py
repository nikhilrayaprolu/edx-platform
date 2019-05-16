from cms.envs.devstack import *

INSTALLED_APPS.remove('openedx.core.djangoapps.datadog.apps.DatadogConfig')

# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/data/uploads/"

# Video settingsp
VIDEO_IMAGE_SETTINGS['STORAGE_KWARGS']['location'] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS['STORAGE_KWARGS']['location'] = MEDIA_ROOT

# Change syslog-based loggers which don't work inside docker containers
LOGGING['handlers']['local'] = {'class': 'logging.NullHandler'}
LOGGING['handlers']['tracking'] = {
    'level': 'DEBUG',
    'class': 'logging.StreamHandler',
    'formatter': 'standard',
}

LOCALE_PATHS.append('/openedx/locale')

# Create folders if necessary
import os
for folder in [LOG_DIR, MEDIA_ROOT, STATIC_ROOT_BASE]:
    if not os.path.exists(folder):
        os.makedirs(folder)
OAUTH_ENFORCE_SECURE = False

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'cache-control',
)
CORS_ORIGIN_WHITELIST = (
    'http://localhost:4200',
    'http://youngsphere.com'
)

DEBUG_TOOLBAR_PATCH_SETTINGS = False


EDX_API_KEY = "test"

MIDDLEWARE_CLASSES += (
    'organizations.middleware.OrganizationMiddleware',
)