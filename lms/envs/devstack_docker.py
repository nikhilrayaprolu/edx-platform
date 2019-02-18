""" Overrides for Docker-based devstack. """

from .devstack import *  # pylint: disable=wildcard-import, unused-wildcard-import

# Docker does not support the syslog socket at /dev/log. Rely on the console.
LOGGING['handlers']['local'] = LOGGING['handlers']['tracking'] = {
    'class': 'logging.NullHandler',
}

LOGGING['loggers']['tracking']['handlers'] = ['console']

LMS_BASE = 'edx.devstack.lms:18000'
CMS_BASE = 'edx.devstack.studio:18010'
SITE_NAME = LMS_BASE
LMS_ROOT_URL = 'http://{}'.format(LMS_BASE)
LMS_INTERNAL_ROOT_URL = LMS_ROOT_URL

ECOMMERCE_PUBLIC_URL_ROOT = 'http://localhost:18130'
ECOMMERCE_API_URL = 'http://edx.devstack.ecommerce:18130/api/v2'

COMMENTS_SERVICE_URL = 'http://edx.devstack.forum:4567'

ENTERPRISE_API_URL = '{}/enterprise/api/v1/'.format(LMS_INTERNAL_ROOT_URL)

CREDENTIALS_INTERNAL_SERVICE_URL = 'http://edx.devstack.credentials:18150'
CREDENTIALS_PUBLIC_SERVICE_URL = 'http://localhost:18150'

OAUTH_OIDC_ISSUER = '{}/oauth2'.format(LMS_ROOT_URL)

DEFAULT_JWT_ISSUER = {
    'ISSUER': OAUTH_OIDC_ISSUER,
    'SECRET_KEY': 'lms-secret',
    'AUDIENCE': 'lms-key',
}
JWT_AUTH.update({
    'JWT_ISSUER': DEFAULT_JWT_ISSUER['ISSUER'],
    'JWT_AUDIENCE': DEFAULT_JWT_ISSUER['AUDIENCE'],
    'JWT_ISSUERS': [
        DEFAULT_JWT_ISSUER,
        RESTRICTED_APPLICATION_JWT_ISSUER,
    ],
})

FEATURES.update({
    'AUTOMATIC_AUTH_FOR_TESTING': True,
    'ENABLE_COURSEWARE_SEARCH': False,
    'ENABLE_COURSE_DISCOVERY': False,
    'ENABLE_DASHBOARD_SEARCH': False,
    'ENABLE_DISCUSSION_SERVICE': True,
    'SHOW_HEADER_LANGUAGE_SELECTOR': True,
    'ENABLE_ENTERPRISE_INTEGRATION': False,
})

ENABLE_MKTG_SITE = os.environ.get('ENABLE_MARKETING_SITE', False)
MARKETING_SITE_ROOT = os.environ.get('MARKETING_SITE_ROOT', 'http://localhost:8080')

MKTG_URLS = {
    'ABOUT': '/about',
    'ACCESSIBILITY': '/accessibility',
    'AFFILIATES': '/affiliate-program',
    'BLOG': '/blog',
    'CAREERS': '/careers',
    'CONTACT': '/support/contact_us',
    'COURSES': '/course',
    'DONATE': '/donate',
    'ENTERPRISE': '/enterprise',
    'FAQ': '/student-faq',
    'HONOR': '/edx-terms-service',
    'HOW_IT_WORKS': '/how-it-works',
    'MEDIA_KIT': '/media-kit',
    'NEWS': '/news-announcements',
    'PRESS': '/press',
    'PRIVACY': '/edx-privacy-policy',
    'ROOT': MARKETING_SITE_ROOT,
    'SCHOOLS': '/schools-partners',
    'SITE_MAP': '/sitemap',
    'TRADEMARKS': '/trademarks',
    'TOS': '/edx-terms-service',
    'TOS_AND_HONOR': '/edx-terms-service',
    'WHAT_IS_VERIFIED_CERT': '/verified-certificate',
}

CREDENTIALS_SERVICE_USERNAME = 'credentials_worker'

COURSE_CATALOG_API_URL = 'http://edx.devstack.discovery:18381/api/v1/'



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
WAGTAIL_SITE_NAME = 'Young Sphere Site'
PUPUT_AS_PLUGIN = True
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
'wagtail.wagtailcore.middleware.SiteMiddleware',

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


