#youngsphere.py
from .devstack import *
import dj_database_url
OAUTH_ENFORCE_SECURE = False

INSTALLED_APPS += (
    'openedx.core.djangoapps.youngsphere.sites',
    'openedx.core.djangoapps.youngsphere.api',
)


CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'cache-control'
)

DEBUG_TOOLBAR_PATCH_SETTINGS = False


AUTHENTICATION_BACKENDS = (
    'organizations.backends.DefaultSiteBackend',
    'organizations.backends.SiteMemberBackend',
    'organizations.backends.OrganizationMemberBackend',
)

EDX_API_KEY = "test"

MIDDLEWARE_CLASSES += (
    'organizations.middleware.OrganizationMiddleware',
)

COURSE_CATALOG_VISIBILITY_PERMISSION = 'see_in_catalog'
COURSE_ABOUT_VISIBILITY_PERMISSION = 'see_about_page'
SEARCH_SKIP_ENROLLMENT_START_DATE_FILTERING = True

if FEATURES.get("ENABLE_TIERS_APP", True):
    TIERS_ORGANIZATION_MODEL = 'organizations.Organization'
    TIERS_EXPIRED_REDIRECT_URL = ENV_TOKENS.get('TIERS_EXPIRED_REDIRECT_URL', None)
    TIERS_ORGANIZATION_TIER_GETTER_NAME = 'get_tier_for_org'

    #TIERS_DATABASE_URL = AUTH_TOKENS.get('TIERS_DATABASE_URL')
    #DATABASES['tiers'] = dj_database_url.parse(TIERS_DATABASE_URL)
    DATABASE_ROUTERS += ['openedx.core.djangoapps.youngsphere.sites.routers.TiersDbRouter']

    MIDDLEWARE_CLASSES += (
        'tiers.middleware.TierMiddleware',
    )

    INSTALLED_APPS += (
        'tiers',
    )

COURSE_TO_CLONE = "course-v1:Appsembler+CC101+2017"

CELERY_ALWAYS_EAGER = True

ALTERNATE_QUEUE_ENVS = ['cms']
ALTERNATE_QUEUES = [
    DEFAULT_PRIORITY_QUEUE.replace(QUEUE_VARIANT, alternate + '.')
    for alternate in ALTERNATE_QUEUE_ENVS
]
CELERY_QUEUES.update(
    {
        alternate: {}
        for alternate in ALTERNATE_QUEUES
        if alternate not in CELERY_QUEUES.keys()
    }
)

CLONE_COURSE_FOR_NEW_SIGNUPS = False
HIJACK_ALLOW_GET_REQUESTS = True
HIJACK_LOGOUT_REDIRECT_URL = '/admin/auth/user'

USE_S3_FOR_CUSTOMER_THEMES = False

DEFAULT_COURSE_MODE_SLUG = ENV_TOKENS.get('EDXAPP_DEFAULT_COURSE_MODE_SLUG', 'audit')
DEFAULT_MODE_NAME_FROM_SLUG = DEFAULT_COURSE_MODE_SLUG.capitalize()

CUSTOM_DOMAINS_REDIRECT_CACHE_TIMEOUT = None  # The length of time we cache Redirect model data
CUSTOM_DOMAINS_REDIRECT_CACHE_KEY_PREFIX = 'custom_domains_redirects'

try:
    from .private import *
except ImportError:
    pass