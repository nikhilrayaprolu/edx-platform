from django.apps import AppConfig

from django.db.models.signals import pre_save


class SitesConfig(AppConfig):
    name = 'openedx.core.djangoapps.youngsphere.sites'
    label = 'youngsphere_sites'

    def ready(self):
        import openedx.core.djangoapps.youngsphere.sites.signals
        #from .models import patched_clear_site_cache
        #pre_save.connect(patched_clear_site_cache, sender='site_configuration.SiteConfiguration')
