from lms.envs.aws import *

FEATURES.update({
    'ENABLE_OAUTH2_PROVIDER': True,
    'ENABLE_MOBILE_REST_API': True,
    'ENABLE_COMBINED_LOGIN_REGISTRATION': True,
    'ENABLE_COMBINED_LOGIN_REGISTRATION_FOOTER': True,

})

INSTALLED_APPS.remove('openedx.core.djangoapps.datadog.apps.DatadogConfig')

# Load module store settings from config files
update_module_store_settings(MODULESTORE, doc_store_settings=DOC_STORE_CONFIG)

# Set uploaded media file path
MEDIA_ROOT = "/openedx/data/uploads/"

# Video settings
VIDEO_IMAGE_SETTINGS['STORAGE_KWARGS']['location'] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS['STORAGE_KWARGS']['location'] = MEDIA_ROOT

# Change syslog-based loggers which don't work inside docker containers
LOGGING['handlers']['local'] = {'class': 'logging.NullHandler'}
LOGGING['handlers']['tracking'] = {
    'level': 'DEBUG',
    'class': 'logging.StreamHandler',
    'formatter': 'standard',
}

# Fix media files paths
VIDEO_IMAGE_SETTINGS['STORAGE_KWARGS']['location'] = MEDIA_ROOT
VIDEO_TRANSCRIPTS_SETTINGS['STORAGE_KWARGS']['location'] = MEDIA_ROOT
PROFILE_IMAGE_BACKEND['options']['location'] = os.path.join(MEDIA_ROOT, 'profile-images/')

ALLOWED_HOSTS = [
    "*",
    ENV_TOKENS.get('LMS_BASE'),
    FEATURES['PREVIEW_LMS_BASE'],
    '127.0.0.1', 'localhost', 'preview.localhost',
    '127.0.0.1:8000', 'localhost:8000', 'preview.localhost:8000',
]

# Required to display all courses on start page
SEARCH_SKIP_ENROLLMENT_START_DATE_FILTERING = True

# Allow insecure oauth2 for local interaction with local containers
OAUTH_ENFORCE_SECURE = False

DEFAULT_FROM_EMAIL = ENV_TOKENS['CONTACT_EMAIL']
DEFAULT_FEEDBACK_EMAIL = ENV_TOKENS['CONTACT_EMAIL']
SERVER_EMAIL = ENV_TOKENS['CONTACT_EMAIL']
TECH_SUPPORT_EMAIL = ENV_TOKENS['CONTACT_EMAIL']
CONTACT_EMAIL = ENV_TOKENS['CONTACT_EMAIL']
BUGS_EMAIL = ENV_TOKENS['CONTACT_EMAIL']
UNIVERSITY_EMAIL = ENV_TOKENS['CONTACT_EMAIL']
PRESS_EMAIL = ENV_TOKENS['CONTACT_EMAIL']
PAYMENT_SUPPORT_EMAIL = ENV_TOKENS['CONTACT_EMAIL']
BULK_EMAIL_DEFAULT_FROM_EMAIL = 'no-reply@' + ENV_TOKENS['LMS_BASE']
API_ACCESS_MANAGER_EMAIL = ENV_TOKENS['CONTACT_EMAIL']
API_ACCESS_FROM_EMAIL = ENV_TOKENS['CONTACT_EMAIL']

ORA2_FILEUPLOAD_BACKEND = 'filesystem'
ORA2_FILEUPLOAD_ROOT = '/openedx/data/ora2'
ORA2_FILEUPLOAD_CACHE_NAME = 'ora2-storage'

LOCALE_PATHS.append('/openedx/locale')

# Create folders if necessary
import os
for folder in [LOG_DIR, MEDIA_ROOT, STATIC_ROOT_BASE, ORA2_FILEUPLOAD_ROOT]:
    if not os.path.exists(folder):
        os.makedirs(folder)

OAUTH_ENFORCE_SECURE = False

INSTALLED_APPS += (
    'openedx.core.djangoapps.youngsphere.api',
    'openedx.core.djangoapps.youngsphere.sites',
'openedx.core.djangoapps.youngsphere.progress',
'openedx.core.djangoapps.youngsphere.social_engagement',
    'rest_framework.authtoken',
'wagtail.wagtailforms',
'wagtail.wagtailredirects',
'wagtail.wagtailembeds',
'wagtail.wagtailsites',
'wagtail.wagtailusers',
'wagtail.wagtailsnippets',
'wagtail.wagtaildocs',
'wagtail.wagtailimages',
'wagtail.wagtailsearch',
'wagtail.wagtailadmin',
'wagtail.wagtailcore',

'modelcluster',
'taggit',

'puput',
'wagtail.contrib.wagtailsitemaps',
'wagtail.contrib.wagtailroutablepage',



)
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

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
    'http://studio.youngsphere.com',
)

DEBUG_TOOLBAR_PATCH_SETTINGS = False


EDX_API_KEY = "test"
WAGTAIL_SITE_NAME = 'Young Sphere Blog'
PUPUT_AS_PLUGIN = True

MIDDLEWARE_CLASSES += (
    'organizations.middleware.OrganizationMiddleware',
'wagtail.wagtailcore.middleware.SiteMiddleware',
'wagtail.wagtailredirects.middleware.RedirectMiddleware',

)
CLONE_COURSE_FOR_NEW_SIGNUPS = False
SESSION_COOKIE_DOMAIN = '.youngsphere.com'