"""
Bare minimum settings for collecting production assets.
"""
from ..common import *
from openedx.core.lib.derived import derive_settings

COMPREHENSIVE_THEME_DIRS.append('/openedx/themes')
STATIC_ROOT_BASE = '/openedx/staticfiles'
STATIC_ROOT = path(STATIC_ROOT_BASE)
WEBPACK_LOADER['DEFAULT']['STATS_FILE'] = STATIC_ROOT / "webpack-stats.json"

SECRET_KEY = 'secret'
XQUEUE_INTERFACE = {
    'django_auth': None,
    'url': None,
}
DATABASES = {
    "default": {},
}


OAUTH_ENFORCE_SECURE = False

INSTALLED_APPS += (
    'openedx.core.djangoapps.youngsphere.sites',
'openedx.core.djangoapps.youngsphere.progress',
'openedx.core.djangoapps.youngsphere.social_engagement',


)

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
)

DEBUG_TOOLBAR_PATCH_SETTINGS = False


EDX_API_KEY = "test"

MIDDLEWARE_CLASSES += (
    'organizations.middleware.OrganizationMiddleware',
)

derive_settings(__name__)


